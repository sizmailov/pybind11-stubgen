#include "modules.h"

#include <Eigen/Core>
#include <pybind11/eigen.h>

void bind_eigen_module(py::module_ &&m) {
    m.def("get_matrix_int", [] { return Eigen::Matrix3i{}; });
    m.def("get_vector_float64", [] { return Eigen::Vector3d{}; });
    m.def("accept_matrix_int", [](Eigen::Matrix3i &) {});
    m.def("accept_vector_float64", [](Eigen::Vector3d &) {});
}
