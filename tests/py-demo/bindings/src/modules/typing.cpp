#include "modules.h"


void bind_typing_module(py::module_&& m) {
    m.def("sequence", [](py::sequence &seq) { return seq; });
}
