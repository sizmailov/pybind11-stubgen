#include "modules.h"

#include <Eigen/Core>
#include <pybind11/eigen.h>

void bind_eigen_module(py::module &&m) {

    using DenseMatrixR = Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
    using DenseMatrixC = Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic>;

    using FixedMatrixR = Eigen::Matrix<float, 5, 6, Eigen::RowMajor>;
    using FixedMatrixC = Eigen::Matrix<float, 5, 6>;
    using FourRowMatrixR = Eigen::Matrix<float, 4, Eigen::Dynamic>;
    using FourColMatrixR = Eigen::Matrix<float, Eigen::Dynamic, 4>;
    using SparseMatrixR = Eigen::SparseMatrix<float, Eigen::RowMajor>;
    using SparseMatrixC = Eigen::SparseMatrix<float>;

    m.def("get_matrix_int", [] { return Eigen::Matrix3i{}; });
    m.def("get_vector_float64", [] { return Eigen::Vector3d{}; });
    m.def("accept_matrix_int", [](Eigen::Matrix3i &) {});
    m.def("accept_vector_float64", [](Eigen::Vector3d &) {});
    m.def("dense_matrix_r", [](DenseMatrixR &m) { return m; });
    m.def("dense_matrix_c", [](DenseMatrixC &m) { return m; });
    m.def("four_row_matrix_r", [](FourRowMatrixR &m) { return m; });
    m.def("four_col_matrix_r", [](FourColMatrixR &m) { return m; });
    m.def("sparse_matrix_r", [](SparseMatrixR &m) { return m; });
    m.def("sparse_matrix_c", [](SparseMatrixC &m) { return m; });

    m.def("fixed_mutator_r", [](const Eigen::Ref<FixedMatrixR> &) {});
    m.def("fixed_mutator_c", [](const Eigen::Ref<FixedMatrixC> &) {});
    m.def("fixed_mutator_a", [](const py::EigenDRef<FixedMatrixC> &) {});
}
