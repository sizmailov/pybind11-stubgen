#include "modules.h"

void bind_typing_module(py::module_ &&m) {
    m.def("get_sequence", [](py::sequence &seq) { return seq; });
    m.def("get_buffer", [](py::buffer &buffer) { return buffer; });
}
