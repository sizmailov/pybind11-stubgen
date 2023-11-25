#include "modules.h"

#include <demo/sublibA/ConsoleColors.h>

void bind_duplicate_enum_module(py::module&&m) {

    py::enum_<demo::sublibA::ConsoleForegroundColorDuplicate>(m, "ConsoleForegroundColor")
        .value("Magenta", demo::sublibA::ConsoleForegroundColorDuplicate::Magenta)
        .export_values();

    m.def(
        "accepts_ambiguous_enum",
        [](const demo::sublibA::ConsoleForegroundColorDuplicate &color) {},
        py::arg("color") = demo::sublibA::ConsoleForegroundColorDuplicate::Magenta);
}
