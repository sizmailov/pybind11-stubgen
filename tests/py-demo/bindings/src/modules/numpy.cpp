#include <pybind11/numpy.h>

#include "modules.h"

void bind_numpy_module(py::module_&&m) {
    {
        m.def("get_ndarray_int", [] { return py::array_t<int>{}; });
        m.def("get_ndarray_float64", [] { return py::array_t<double>{}; });
        m.def("accept_ndarray_int", [](py::array_t<int> &) {});
        m.def("accept_ndarray_float64", [](py::array_t<double> &) {});
    }
}
