#include <pybind11/typing.h>

#include "modules.h"

#include <demo/sublibA/add.h>

namespace {
void generic(const py::args &args, const py::kwargs &kwargs) {}
}; // namespace

void bind_functions_module(py::module_ &&m) {
    m.def("add", demo::sublibA::add);
    {

        m.def(
            "mul",
            [](int x, int y) { return x * y; },
            "Multiply x and y (int)",
            py::arg("x"),
            py::arg("y"));
        m.def(
            "mul",
            [](double p, double q) { return p * q; },
            "Multiply p and q (double)",
            py::arg("p"),
            py::arg("q"));
    }

    m.def("func_w_anon_args", [](int x, int y, int z) {});

    m.def(
        "func_w_named_pos_args",
        [](int x, int y, int z) {},
        py::arg("x"),
        py::arg("y"),
        py::arg("z"),
        py::pos_only());

    m.def(
        "pos_kw_only_mix",
        [](int i, int j, int k) { return py::make_tuple(i, j, k); },
        py::arg("i"),
        py::pos_only(),
        py::arg("j"),
        py::kw_only(),
        py::arg("k"));
    m.def("generic", &generic);

    m.def(
        "pos_kw_only_variadic_mix",
        [](int i, int j, py::args &, int k, py::kwargs &) { return py::make_tuple(i, j, k); },
        py::arg("i"),
        py::pos_only(),
        py::arg("j"),
        py::kw_only(),
        py::arg("k"));

    m.def("accept_callable", [](py::function &callable) { return callable(); });
    m.def("accept_py_object", [](py::object &object) { return py::str(object); });
    m.def("accept_py_handle", [](py::handle &handle) { return py::str(handle); });

    m.def("accept_annotated_callable",
          [](py::typing::Callable<int(int, int)> &callable) { return callable(13, 42); });
}
