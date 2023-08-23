#include "modules.h"

namespace {

struct Unbound {};

enum Enum { ONE = 1, TWO = 2 };

} // namespace

void bind_flawed_bindings_module(py::module_&& m) {
    // This submodule will have C++ signatures in python docstrings to emulate
    // common mistakes in using pybind11
    m.def("get_unbound_type", [] { return Unbound{}; });
    m.def("accept_unbound_type", [](std::pair<Unbound, int>) { return 0; });
    m.def("accept_unbound_enum", [](Enum) { return 0; });

    py::class_<Unbound>(m, "Unbound");
    py::class_<Enum>(m, "Enum");
    m.def(
        "accept_unbound_type_defaulted", [](Unbound) { return 0; }, py::arg("x") = Unbound{});
    m.def(
        "accept_unbound_enum_defaulted", [](Enum) { return 0; }, py::arg("x") = Enum::ONE);
}
