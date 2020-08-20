from typing import Optional, Callable, Iterator, Iterable, List, Set, Mapping, Tuple, Any, Dict
from functools import cmp_to_key
import warnings
import importlib
import itertools
import inspect
import logging
import sys
import os
import re
from argparse import ArgumentParser

logger = logging.getLogger(__name__)

_visited_objects = []


class DirectoryWalkerGuard(object):

    def __init__(self, dirname):
        self.dirname = dirname

    def __enter__(self):
        if not os.path.exists(self.dirname):
            os.mkdir(self.dirname)

        assert os.path.isdir(self.dirname)

        os.chdir(self.dirname)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(os.path.pardir)


class FunctionSignature(object):

    def __init__(self, name, args='*args, **kwargs', rtype='None'):
        self.name = name
        self.args = args
        self.rtype = rtype

    def __eq__(self, other):
        return isinstance(other, FunctionSignature) and (self.name, self.args, self.rtype) == (
            other.name, other.args, other.rtype)

    def __hash__(self):
        return hash((self.name, self.args, self.rtype))

    def split_arguments(self):
        if len(self.args.strip()) == 0:
            return []

        prev_stop = 0
        brackets = 0
        splitted_args = []

        for i, c in enumerate(self.args):
            if c == "[":
                brackets += 1
            elif c == "]":
                brackets -= 1
                assert brackets >= 0
            elif c == "," and brackets == 0:
                splitted_args.append(self.args[prev_stop:i])
                prev_stop = i + 1

        splitted_args.append(self.args[prev_stop:])
        assert brackets == 0
        return splitted_args

    @staticmethod
    def argument_type(arg):
        return arg.split(":")[-1].strip()

    def get_all_involved_types(self):
        types = []
        for t in [self.rtype] + self.split_arguments():
            types.extend([m[0] for m in
                          re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*)", self.argument_type(t))
                          ])
        return types


class PropertySignature(object):
    NONE = 0
    READ_ONLY = 1
    WRITE_ONLY = 2
    READ_WRITE = READ_ONLY | WRITE_ONLY

    def __init__(self, rtype, setter_args, access_type):
        self.rtype = rtype
        self.setter_args = setter_args
        self.access_type = access_type

    @property
    def setter_arg_type(self):
        return FunctionSignature.argument_type(FunctionSignature('name', self.setter_args).split_arguments()[1])


def replace_numpy_array(match_obj):
    numpy_type = match_obj.group("type")
    # pybind always append size of data type
    if numpy_type in ['int8', 'int16', 'int32', 'int64',
                      'float16', 'float32', 'float64',
                      'complex32', 'complex64', 'longcomplex'
                      ]:
        numpy_type = "numpy." + numpy_type

    shape = match_obj.group("shape")
    if shape:
        shape = ", _Shape[{}]".format(shape)
    else:
        shape = ""
    result = r"numpy.ndarray[{type}{shape}]".format(type=numpy_type, shape=shape)
    return result


def replace_typing_types(match):
    # pybind used to have iterator/iterable in place of Iterator/Iterable
    return "typing." + match.group('type').capitalize()


class StubsGenerator(object):
    INDENT = " " * 4

    GLOBAL_CLASSNAME_REPLACEMENTS = {
        re.compile(r"numpy.ndarray\[(?P<type>[^\[\]]+)(\[(?P<shape>[^\[\]]+)\])?\]"): replace_numpy_array,
        re.compile(r"(?<!\w)(?P<type>Callable|Dict|[Ii]terator|[Ii]terable|List|Optional|Set|Tuple|Union')(?!\w)"): replace_typing_types
    }

    def parse(self):
        raise NotImplementedError

    def to_lines(self):  # type: () -> List[str]
        raise NotImplementedError

    @staticmethod
    def _indent(line):  # type: (str) -> str
        return StubsGenerator.INDENT + line

    @staticmethod
    def indent(lines):  # type: (str) -> str
        lines = lines.split("\n")
        lines = [StubsGenerator._indent(l) if l else l for l in lines]
        return "\n".join(lines)

    @staticmethod
    def fully_qualified_name(klass):
        module_name = klass.__module__ if hasattr(klass, '__module__') else None
        class_name = getattr(klass, "__qualname__", klass.__name__)

        if module_name == "builtins":
            return class_name
        else:
            return "{module}.{klass}".format(
                module=module_name,
                klass=class_name)

    @staticmethod
    def apply_classname_replacements(s):  # type: (str) -> Any
        for k, v in StubsGenerator.GLOBAL_CLASSNAME_REPLACEMENTS.items():
            s = k.sub(v, s)
        return s

    @staticmethod
    def function_signatures_from_docstring(name, func, module_name):  # type: (Any, str) -> List[FunctionSignature]
        try:
            no_parentheses = r"[^()]*"
            parentheses_one_fold = r"({nopar}(\({nopar}\))?)*".format(nopar=no_parentheses)
            parentheses_two_fold = r"({nopar}(\({par1}\))?)*".format(par1=parentheses_one_fold, nopar=no_parentheses)
            parentheses_three_fold = r"({nopar}(\({par2}\))?)*".format(par2=parentheses_two_fold, nopar=no_parentheses)
            signature_regex = r"(\s*(?P<overload_number>\d+).)" \
                              r"?\s*{name}\s*\((?P<args>{balanced_parentheses})\)" \
                              r"\s*->\s*" \
                              r"(?P<rtype>[^\(\)]+)\s*".format(name=name,
                                                               balanced_parentheses=parentheses_three_fold)
            doc_lines = func.__doc__
            signatures = []
            for line in doc_lines.split("\n"):
                m = re.match(signature_regex, line)
                if m:
                    args = m.group("args")
                    rtype = m.group("rtype")
                    signatures.append(FunctionSignature(name, args, rtype))

            # strip module name if provided
            if module_name:
                for sig in signatures:
                    regex = r"{}\.(\w+)".format(module_name.replace(".", r"\."))
                    sig.args = re.sub(regex, r"\g<1>", sig.args)
                    sig.rtype = re.sub(regex, r"\g<1>", sig.rtype)

            for sig in signatures:
                sig.args = StubsGenerator.apply_classname_replacements(sig.args)
                sig.rtype = StubsGenerator.apply_classname_replacements(sig.rtype)

            return sorted(list(set(signatures)),
                          key=lambda fs: fs.args)
        except AttributeError:
            return []

    @staticmethod
    def property_signature_from_docstring(prop, module_name):  # type:  (Any, str)-> PropertySignature

        getter_rtype = "None"
        setter_args = "None"
        access_type = PropertySignature.NONE

        strip_module_name = module_name is not None

        if hasattr(prop, "fget") and prop.fget is not None:
            access_type |= PropertySignature.READ_ONLY
            if hasattr(prop.fget, "__doc__") and prop.fget.__doc__ is not None:
                for line in prop.fget.__doc__.split("\n"):
                    if strip_module_name:
                        line = line.replace(module_name + ".", "")
                    m = re.match(r"\s*\((?P<args>[^()]*)\)\s*->\s*(?P<rtype>[^()]+)\s*", line)
                    if m:
                        getter_rtype = m.group("rtype")
                        break

        if hasattr(prop, "fset") and prop.fset is not None:
            access_type |= PropertySignature.WRITE_ONLY
            if hasattr(prop.fset, "__doc__") and prop.fset.__doc__ is not None:
                for line in prop.fset.__doc__.split("\n"):
                    if strip_module_name:
                        line = line.replace(module_name + ".", "")
                    m = re.match(r"\s*\((?P<args>[^()]*)\)\s*->\s*(?P<rtype>[^()]+)\s*", line)
                    if m:
                        args = m.group("args")
                        # replace first argument with self
                        setter_args = ",".join(["self"] + args.split(",")[1:])
                        break
        getter_rtype = StubsGenerator.apply_classname_replacements(getter_rtype)
        setter_args = StubsGenerator.apply_classname_replacements(setter_args)
        return PropertySignature(getter_rtype, setter_args, access_type)

    @staticmethod
    def remove_signatures(docstring):  # type: (str) ->str

        if docstring is None:
            return ""

        signature_regex = r"(\s*(?P<overload_number>\d+).\s*)" \
                          r"?{name}\s*\((?P<args>[^\(\)]*)\)\s*(->\s*(?P<rtype>[^\(\)]+)\s*)?".format(name=r"\w+")

        lines = docstring.split("\n\n")
        lines = filter(lambda line: line != "Overloaded function.", lines)

        return "\n\n".join(filter(lambda line: not re.match(signature_regex, line), lines))

    @staticmethod
    def sanitize_docstring(docstring):  # type: (str) ->str
        docstring = StubsGenerator.remove_signatures(docstring)
        docstring = docstring.rstrip("\n")

        if docstring and re.match(r"^\s*$", docstring):
            docstring = ""

        return docstring

    @staticmethod
    def format_docstring(docstring):
        return StubsGenerator.indent('"""\n{}\n"""'.format(docstring.strip("\n")))


class AttributeStubsGenerator(StubsGenerator):
    def __init__(self, name, attribute):  # type: (str, Any)-> None
        self.name = name
        self.attr = attribute

    def parse(self):
        if self in _visited_objects:
            return
        _visited_objects.append(self)

    def is_safe_to_use_repr(self, value):
        if isinstance(value, (int, str)):
            return True
        if isinstance(value, (float, complex)):
            try:
                eval(repr(value))
                return True
            except (SyntaxError, NameError):
                return False
        if isinstance(value, (list, tuple, set)):
            for x in value:
                if not self.is_safe_to_use_repr(x):
                    return False
            return True
        if isinstance(value, dict):
            for k, v in value.items():
                if not self.is_safe_to_use_repr(k) or not self.is_safe_to_use_repr(v):
                    return False
            return True
        return False

    def to_lines(self):  # type: () -> List[str]
        if self.is_safe_to_use_repr(self.attr):
            return [
                "{name} = {repr}".format(
                    name=self.name,
                    repr=repr(self.attr)
                )
            ]

        value_lines = repr(self.attr).split("\n")
        if len(value_lines) == 1:
            value = value_lines[0]
            # remove random address from <foo.Foo object at 0x1234>
            value = re.sub(r" at 0x[0-9a-fA-F]+>", ">", value)
            typename = self.fully_qualified_name(type(self.attr))
            if value == "<{typename} object>".format(typename=typename):
                value_comment = ""
            else:
                value_comment = " # value = {value}".format(value=value)
            return [
                "{name}: {typename}{value_comment}".format(
                    name=self.name,
                    typename=typename,
                    value_comment=value_comment)
            ]
        else:
            return [
                       "{name}: {typename} # value = ".format(
                           name=self.name,
                           typename=str(type(self.attr)))
                   ] \
                   + ['"""'] \
                   + [l.replace('"""', r'\"\"\"') for l in value_lines] \
                   + ['"""']

    def get_involved_modules_names(self):  # type: () -> Set[str]
        return set((self.attr.__class__.__module__,))


class FreeFunctionStubsGenerator(StubsGenerator):
    def __init__(self, name, free_function, module_name):
        self.name = name
        self.member = free_function
        self.module_name = module_name
        self.signatures = []  # type:  List[FunctionSignature]

    def parse(self):
        self.signatures = self.function_signatures_from_docstring(self.name, self.member, self.module_name)

    def to_lines(self):  # type: () -> List[str]
        result = []
        docstring = self.sanitize_docstring(self.member.__doc__)
        if not docstring and not (self.name.startswith("__") and self.name.endswith("__")):
            logger.debug("Docstring is empty for '%s'" % self.fully_qualified_name(self.member))
        for sig in self.signatures:
            if len(self.signatures) > 1:
                result.append("@typing.overload")
            result.append("def {name}({args}) -> {rtype}:".format(
                name=sig.name,
                args=sig.args,
                rtype=sig.rtype
            ))
            if docstring:
                result.append(self.format_docstring(docstring))
                docstring = None  # don't print docstring for other overloads
            else:
                result.append(self.indent("pass"))

        return result

    def get_involved_modules_names(self):  # type: () -> Set[str]
        involved_modules_names = set()
        for s in self.signatures:  # type: FunctionSignature
            for t in s.get_all_involved_types():  # type: str
                try:
                    i = t.rindex(".")
                    involved_modules_names.add(t[:i])
                except ValueError:
                    pass
        return involved_modules_names


class ClassMemberStubsGenerator(FreeFunctionStubsGenerator):
    def __init__(self, name, free_function, module_name):
        super(ClassMemberStubsGenerator, self).__init__(name, free_function, module_name)

    def to_lines(self):  # type: () -> List[str]
        result = []
        docstring = self.sanitize_docstring(self.member.__doc__)
        if not docstring and not (self.name.startswith("__") and self.name.endswith("__")):
            logger.debug("Docstring is empty for '%s'" % self.fully_qualified_name(self.member))
        for sig in self.signatures:
            args = sig.args
            if not args.strip().startswith("self"):
                result.append("@staticmethod")
            else:
                # remove type of self
                args = ",".join(["self"] + sig.split_arguments()[1:])
            if len(self.signatures) > 1:
                result.append("@typing.overload")

            result.append("def {name}({args}) -> {rtype}: {ellipsis}".format(
                name=sig.name,
                args=args,
                rtype=sig.rtype,
                ellipsis="" if docstring else "..."
            ))
            if docstring:
                result.append(self.format_docstring(docstring))
                docstring = None  # don't print docstring for other overloads
        return result


class PropertyStubsGenerator(StubsGenerator):
    def __init__(self, name, prop, module_name):
        self.name = name
        self.prop = prop
        self.module_name = module_name
        self.signature = None  # type: PropertySignature

    def parse(self):
        self.signature = self.property_signature_from_docstring(self.prop, self.module_name)

    def to_lines(self):  # type: () -> List[str]

        docstring = self.sanitize_docstring(self.prop.__doc__)
        docstring_prop = "\n\n".join([docstring, ":type: {rtype}".format(rtype=self.signature.rtype)])

        result = ["@property",
                  "def {field_name}(self) -> {rtype}:".format(field_name=self.name, rtype=self.signature.rtype),
                  self.format_docstring(docstring_prop)]

        if self.signature.setter_args != "None":
            result.append("@{field_name}.setter".format(field_name=self.name))
            result.append(
                "def {field_name}({args}) -> None:".format(field_name=self.name, args=self.signature.setter_args))
            if docstring:
                result.append(self.format_docstring(docstring))
            else:
                result.append(self.indent("pass"))

        return result


class ClassStubsGenerator(StubsGenerator):
    ATTRIBUTES_BLACKLIST = ("__class__", "__module__", "__qualname__", "__dict__", "__weakref__", "__annotations__")
    METHODS_BLACKLIST = ("__dir__", "__sizeof__")
    BASE_CLASS_BLACKLIST = ("pybind11_object", "object")
    CLASS_NAME_BLACKLIST = ("pybind11_type",)

    def __init__(self,
                 klass,
                 attributes_blacklist=ATTRIBUTES_BLACKLIST,
                 base_class_blacklist=BASE_CLASS_BLACKLIST,
                 methods_blacklist=METHODS_BLACKLIST,
                 class_name_blacklist=CLASS_NAME_BLACKLIST
                 ):
        self.klass = klass
        assert inspect.isclass(klass)

        self.doc_string = None  # type: Optional[str]

        self.classes = []  # type: List[ClassStubsGenerator]
        self.fields = []  # type: List[AttributeStubsGenerator]
        self.properties = []  # type: List[PropertyStubsGenerator]
        self.methods = []  # type: List[ClassMemberStubsGenerator]

        self.base_classes = []
        self.involved_modules_names = set()  # Set[str]

        self.attributes_blacklist = attributes_blacklist
        self.base_class_blacklist = base_class_blacklist
        self.methods_blacklist = methods_blacklist
        self.class_name_blacklist = class_name_blacklist

    def get_involved_modules_names(self):
        return self.involved_modules_names

    def parse(self):
        if self.klass in _visited_objects:
            return
        _visited_objects.append(self.klass)

        bases = inspect.getmro(self.klass)[1:]

        def is_base_member(name, member):
            for base in bases:
                if hasattr(base, name) and getattr(base, name) is member:
                    return True
            return False

        for name, member in inspect.getmembers(self.klass):
            # check if attribute is in __dict__ (fast path) before slower search in base classes
            if name not in self.klass.__dict__ and is_base_member(name, member):
                continue
            if inspect.isroutine(member):
                self.methods.append(ClassMemberStubsGenerator(name, member, self.klass.__module__))
            elif name != '__class__' and inspect.isclass(member):
                if member.__name__ not in self.class_name_blacklist:
                    self.classes.append(ClassStubsGenerator(member))
            elif isinstance(member, property):
                self.properties.append(PropertyStubsGenerator(name, member, self.klass.__module__))
            elif name == "__doc__":
                self.doc_string = member
            elif name not in self.attributes_blacklist:
                self.fields.append(AttributeStubsGenerator(name, member))
                # logger.warning("Unknown member %s type : `%s` " % (name, str(type(member))))

        for x in itertools.chain(self.classes,
                                 self.methods,
                                 self.properties,
                                 self.fields):
            x.parse()

        for B in bases:
            if B.__name__ != self.klass.__name__ and B.__name__ not in self.base_class_blacklist:
                self.base_classes.append(B)
                self.involved_modules_names.add(B.__module__)

        for f in self.methods:  # type: ClassMemberStubsGenerator
            self.involved_modules_names |= f.get_involved_modules_names()

    def to_lines(self):  # type: () -> List[str]

        def strip_current_module_name(obj, module_name):
            regex = r"{}\.(\w+)".format(module_name.replace(".", r"\."))
            return re.sub(regex, r"\g<1>", obj)

        base_classes_list = [
            strip_current_module_name(self.fully_qualified_name(b), self.klass.__module__)
            for b in self.base_classes
        ]
        result = [
            "class {class_name}({base_classes_list}):{doc_string}".format(
                class_name=self.klass.__name__,
                base_classes_list=", ".join(base_classes_list),
                doc_string='\n' + self.format_docstring(self.doc_string)
                if self.doc_string else "",
            ),
        ]
        for cl in self.classes:
            result.extend(map(self.indent, cl.to_lines()))

        for f in self.methods:
            if f.name not in self.methods_blacklist:
                result.extend(map(self.indent, f.to_lines()))

        for p in self.properties:
            result.extend(map(self.indent, p.to_lines()))

        for p in self.fields:
            result.extend(map(self.indent, p.to_lines()))

        result.append(self.indent("pass"))
        return result


class ModuleStubsGenerator(StubsGenerator):
    CLASS_NAME_BLACKLIST = ClassStubsGenerator.CLASS_NAME_BLACKLIST
    ATTRIBUTES_BLACKLIST = ("__file__", "__loader__", "__name__", "__package__",
                            "__spec__", "__path__", "__cached__", "__builtins__")

    def __init__(self, module_or_module_name,
                 attributes_blacklist=ATTRIBUTES_BLACKLIST,
                 class_name_blacklist=CLASS_NAME_BLACKLIST
                 ):
        if isinstance(module_or_module_name, str):
            self.module = importlib.import_module(module_or_module_name)
        else:
            self.module = module_or_module_name
            assert inspect.ismodule(self.module)

        self.doc_string = None  # type: Optional[str]
        self.classes = []  # type: List[ClassStubsGenerator]
        self.free_functions = []  # type: List[FreeFunctionStubsGenerator]
        self.submodules = []  # type: List[ModuleStubsGenerator]
        self.imported_modules = []  # type: List[str]
        self.imported_classes = {}  # type: Dict[str, type]
        self.attributes = []  # type: List[AttributeStubsGenerator]
        self.stub_suffix = ""
        self.write_setup_py = False

        self.attributes_blacklist = attributes_blacklist
        self.class_name_blacklist = class_name_blacklist

    def parse(self):
        if self.module in _visited_objects:
            return
        _visited_objects.append(self.module)
        logger.info("Parsing '%s' module" % self.module.__name__)
        for name, member in inspect.getmembers(self.module):
            if inspect.ismodule(member):
                m = ModuleStubsGenerator(member)
                if m.module.__name__.split('.')[:-1] == self.module.__name__.split('.'):
                    self.submodules.append(m)
                else:
                    self.imported_modules += [m.module.__name__]
                    logger.debug("Skip '%s' module while parsing '%s' " % (m.module.__name__, self.module.__name__))
            elif inspect.isbuiltin(member) or inspect.isfunction(member):
                self.free_functions.append(FreeFunctionStubsGenerator(name, member, self.module.__name__))
            elif inspect.isclass(member):
                if member.__module__ == self.module.__name__:
                    if member.__name__ not in self.class_name_blacklist:
                        self.classes.append(ClassStubsGenerator(member))
                else:
                    self.imported_classes[name] = member
            elif name == "__doc__":
                self.doc_string = member
            elif name not in self.attributes_blacklist:
                self.attributes.append(AttributeStubsGenerator(name, member))

        for x in itertools.chain(self.submodules,
                                 self.classes,
                                 self.free_functions,
                                 self.attributes):
            x.parse()

        def class_ordering(a, b):  # type: (ClassStubsGenerator, ClassStubsGenerator) -> int
            if a.klass is b.klass:
                return 0
            if issubclass(a.klass, b.klass):
                return -1
            if issubclass(b.klass, a.klass):
                return 1
            return 0

        # reorder classes so base classes would be printed before derived
        # print([ k.klass.__name__ for k in self.classes ])
        for i in range(len(self.classes)):
            for j in range(i + 1, len(self.classes)):
                if class_ordering(self.classes[i], self.classes[j]) < 0:
                    t = self.classes[i]
                    self.classes[i] = self.classes[j]
                    self.classes[j] = t
        # print( [ k.klass.__name__ for k in self.classes ] )

    def get_involved_modules_names(self):
        result = set(self.imported_modules)

        for attr in self.attributes:
            result |= attr.get_involved_modules_names()

        for C in self.classes:  # type: ClassStubsGenerator
            result |= C.get_involved_modules_names()

        for f in self.free_functions:  # type: FreeFunctionStubsGenerator
            result |= f.get_involved_modules_names()

        return set(result) - {"builtins", 'typing', self.module.__name__}

    def to_lines(self):  # type: () -> List[str]

        result = []

        if self.doc_string:
            result += ['"""' + self.doc_string.replace('"""', r'\"\"\"') + '"""']

        result += [
            "import {}".format(self.module.__name__)
        ]

        # import everything from typing
        result += [
            "import typing"
        ]

        for name, class_ in self.imported_classes.items():
            class_name = getattr(class_, "__qualname__", class_.__name__)
            if name == class_name:
                suffix = ""
            else:
                suffix = " as {}".format(name)
            result += [
                'from {} import {}{}'.format(class_.__module__, class_name, suffix)
            ]

        # import used packages
        used_modules = sorted(self.get_involved_modules_names())
        if used_modules:
            # result.append("if TYPE_CHECKING:")
            # result.extend(map(self.indent, map(lambda m: "import {}".format(m), used_modules)))
            result.extend(map(lambda mod: "import {}".format(mod), used_modules))

        if "numpy" in used_modules:
            result += [
                "_Shape = typing.Tuple[int, ...]"
            ]

        # define __all__

        _all_ = []
        for name in self.imported_classes.keys():
            _all_.append(name)

        for c in self.classes:
            _all_.append(c.klass.__name__)

        for f in self.free_functions:
            _all_.append(f.name)

        for m in self.submodules:
            _all_.append(m.short_name)

        for a in self.attributes:
            _all_.append(a.name)

        all_is_defined = False

        for attr in self.attributes:
            if attr.name == "__all__":
                all_is_defined = True

        if not all_is_defined:
            result.append("__all__  = [\n" + ",\n".join(map(lambda s: '"%s"' % s, _all_)) + "\n]")

        for x in itertools.chain(self.classes,
                                 self.free_functions,
                                 self.attributes):
            result.extend(x.to_lines())
        result.append("")  # Newline at EOF
        return result

    @property
    def short_name(self):
        return self.module.__name__.split(".")[-1]

    def write(self):
        if not os.path.exists(self.short_name + self.stub_suffix):
            logger.info("mkdir `%s`" % (self.short_name + self.stub_suffix))
            os.mkdir(self.short_name + self.stub_suffix)

        with DirectoryWalkerGuard(self.short_name + self.stub_suffix):
            with open("__init__.pyi", "w") as init_pyi:
                init_pyi.write("\n".join(self.to_lines()))
            for m in self.submodules:
                m.write()

            if self.write_setup_py:
                with open("setup.py", "w") as setuppy:
                    setuppy.write("""from setuptools import setup
import os


def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, '', 1)
            stubs.append(path)
    return dict(package=stubs)


setup(
    name='{package_name}-stubs',
    maintainer="{package_name} Developers",
    maintainer_email="example@python.org",
    description="PEP 561 type stubs for {package_name}",
    version='1.0',
    packages=['{package_name}-stubs'],
    # PEP 561 requires these
    install_requires=['{package_name}'],
    package_data=find_stubs('{package_name}-stubs'),
)""".format(package_name=self.short_name))


def recursive_mkdir_walker(subdirs, callback):  # type: (List[str], Callable) -> None
    if len(subdirs) == 0:
        callback()
    else:
        if not os.path.exists(subdirs[0]):
            os.mkdir(subdirs[0])
        with DirectoryWalkerGuard(subdirs[0]):
            recursive_mkdir_walker(subdirs[1:], callback)


def main():
    parser = ArgumentParser(prog='pybind11-stubgen', description="Generates stubs for specified modules")
    parser.add_argument("-o", "--output-dir", help="the root directory for output stubs", default="./stubs")
    parser.add_argument("--root-module-suffix", type=str, default="-stubs", dest='root_module_suffix',
                        help="optional suffix to disambiguate from the "
                             "original package")
    parser.add_argument("--root_module_suffix", type=str, default=None, dest='root_module_suffix_deprecated',
                        help="Deprecated.  Use `--root-module-suffix`")
    parser.add_argument("--no-setup-py", action='store_true')
    parser.add_argument("module_names", nargs="+", metavar="MODULE_NAME", type=str, help="modules names")
    parser.add_argument("--log-level", default="WARNING", help="Set output log level")

    sys_args = parser.parse_args()
    if sys_args.root_module_suffix_deprecated is not None:
        sys_args.root_module_suffix = sys_args.root_module_suffix_deprecated
        warnings.warn("`--root_module_suffix` is deprecated in favor of `--root-module-suffix`", FutureWarning)

    stderr_handler = logging.StreamHandler(sys.stderr)
    handlers = [stderr_handler]

    logging.basicConfig(
        level=logging.getLevelName(sys_args.log_level),
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=handlers
    )

    output_path = sys_args.output_dir

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    with DirectoryWalkerGuard(output_path):
        for _module_name in sys_args.module_names:
            _module = ModuleStubsGenerator(_module_name)
            _module.parse()
            _module.stub_suffix = sys_args.root_module_suffix
            _module.write_setup_py = not sys_args.no_setup_py
            recursive_mkdir_walker(_module_name.split(".")[:-1], lambda: _module.write())


if __name__ == "__main__":
    main()
