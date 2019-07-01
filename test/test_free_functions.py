import subprocess
import os
import functools


class mypy_check:
    script_preamble = ""
    script = ""
    returncode = -1
    stdout = ""
    stderr = ""
    env = os.environ

    def __init__(self, script, env=None):
        self.script = script
        if env is None:
            self.env = mypy_check.env
        else:
            self.env = env

    def run(self):
        proc = subprocess.Popen([
            "mypy",
            "--command", self.script_preamble + "\n" + self.script
        ], env=self.env)

        self.stdout, self.stderr = proc.communicate()
        self.returncode = proc.returncode


def mypy_check_success(script, env=None):
    check = mypy_check(script, env)
    check.run()
    assert check.returncode == 0, """Script did not pass MYPY check
Script:
{script}
MYPY stdout:
{stdout}    
MYPY stderr:
{stderr}
""".format(script=script, stderr=check.stderr, stdout=check.stdout)


def mypy_check_failure(script, env=None, err_msg=None):
    check = mypy_check(script, env)
    check.run()
    assert check.returncode != 0, """Script passed MYPY check
Script:
{script}
MYPY stdout:
{stdout}    
MYPY stderr:
{stderr}
""".format(script=script, stderr=check.stderr, stdout=check.stdout)
    if err_msg is not None:
        assert err_msg in check.stderr, """MYPY check does not contain `{err_msg}`
        Script:
        {script}
        MYPY stdout:
        {stdout}    
        MYPY stderr:
        {stderr}
        """.format(script=script, stderr=check.stderr, stdout=check.stdout, err_msg=err_msg)


class PreambleGuard:

    def __init__(self, preamble):
        self.preamble = preamble

    def __enter__(self):
        self.old_preamble = mypy_check.script_preamble
        mypy_check.script_preamble = self.preamble

    def __exit__(self, exc_type, exc_val, exc_tb):
        mypy_check.script_preamble = self.old_preamble


class EnvGuard:

    def __init__(self, env):
        self.env = env

    def __enter__(self):
        self.old_env = mypy_check.env
        mypy_check.env = self.env

    def __exit__(self, exc_type, exc_val, exc_tb):
        mypy_check.env = self.old_env


def with_preamble_env(preamble, add_env):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            env = os.environ.copy()
            env.update(add_env)
            with EnvGuard(env), PreambleGuard(preamble):
                func()

        return wrapper

    return decorator


python3_module = with_preamble_env("from python3_module import *", {"MYPYPATH": "./stubs"})


@python3_module
def test_1():
    mypy_check_success("accept_foo(Foo())")


@python3_module
def test_2():
    mypy_check_failure("accept_foo(Bar())")


@python3_module
def test_3():
    mypy_check_failure("accept_foo(Bar())")
