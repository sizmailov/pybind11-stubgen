import logging, sys, os
from argparse import ArgumentParser
from pybind11_stubgen import DirectoryWalkerGuard, ModuleStubsGenerator, recursive_mkdir_walker


def main():
    parser = ArgumentParser(description="Generates stubs for specified modules")
    parser.add_argument("-o", "--output-dir", dest="output_dir",
                        help="the root directory for output stubs", default="./stubs")
    parser.add_argument("--root_module_suffix", type=str, default="-stubs",
                        help="optional suffix to disambiguate from the "
                             "original package")
    parser.add_argument("--no-setup-py", action='store_true')
    parser.add_argument("module_names", nargs="+", metavar="MODULE_NAME", type=str, help="modules names")
    parser.add_argument("--log-level", dest="log_level", default="WARNING",
                        help="Set debug output level")

    sys_args = parser.parse_args()

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
