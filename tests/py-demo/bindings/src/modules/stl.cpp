#include <pybind11/complex.h>
#include <pybind11/stl.h>

#include "modules.h"

#include <complex>
#include <map>
#include <variant>

void bind_stl_module(py::module_ &&m) {
    m.def("std_map", [] { return std::map<int, std::complex<double>>{}; });
    m.def("std_vector", [] { return std::vector<std::pair<int, double>>{}; });
    m.def("std_array", [](const std::array<int, 3> &a) { return a; });
    m.def("std_variant", [](const std::variant<int, float, std::pair<int, int>> &) {});
    m.def("std_optional", [](const std::optional<int> &) {});
}
