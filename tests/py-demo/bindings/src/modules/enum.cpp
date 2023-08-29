#include "modules.h"

#include <demo/sublibA/ConsoleColors.h>

void bind_enum_module(py::module_&&m) {

    py::enum_<demo::sublibA::ConsoleForegroundColor>(m, "ConsoleForegroundColor")
        .value("Green", demo::sublibA::ConsoleForegroundColor::Green)
        .value("Yellow", demo::sublibA::ConsoleForegroundColor::Yellow)
        .value("Blue", demo::sublibA::ConsoleForegroundColor::Blue)
        .value("Magenta", demo::sublibA::ConsoleForegroundColor::Magenta)
        .export_values();

    m.def(
        "accept_defaulted_enum",
        [](const demo::sublibA::ConsoleForegroundColor &color) {},
        py::arg("color") = demo::sublibA::ConsoleForegroundColor::Blue);
}
