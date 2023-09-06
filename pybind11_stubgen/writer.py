from __future__ import annotations

from pathlib import Path

from pybind11_stubgen.printer import Printer
from pybind11_stubgen.structs import Module


class Writer:
    def __init__(self, stub_ext: str = "pyi"):
        # assert stub_extension in ["pyi", "py"]
        self.stub_ext: str = stub_ext

    def write_module(
        self, module: Module, printer: Printer, to: Path, sub_dir: Path | None = None
    ):
        assert to.exists()
        assert to.is_dir()
        if module.sub_modules or sub_dir is not None:
            if sub_dir is None:
                sub_dir = Path(module.name)
            module_dir = to / sub_dir
            module_dir.mkdir(exist_ok=True)
            module_file = module_dir / f"__init__.{self.stub_ext}"
        else:
            module_file = to / f"{module.name}.{self.stub_ext}"
        with open(module_file, "w", encoding="utf-8") as f:
            f.writelines(line + "\n" for line in printer.print_module(module))

        for sub_module in module.sub_modules:
            self.write_module(sub_module, printer, to=module_dir)
