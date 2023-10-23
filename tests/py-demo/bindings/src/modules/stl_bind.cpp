#include <pybind11/stl_bind.h>
#include <pybind11/complex.h>
#include "modules.h"

#include <complex>
#include <map>

void bind_stl_bind_module(py::module&&m) {
    py::bind_vector<std::vector<std::pair<std::string, double>>>(m, "VectorPairStringDouble");
    py::bind_map<std::map<std::string, std::complex<double>>>(m, "MapStringComplex");

    m.def("get_complex_map", [] { return std::map<std::string, std::complex<double>>{}; });
    m.def("get_vector_of_pairs", [] { return std::vector<std::pair<std::string, double>>{}; });
}
