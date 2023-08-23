#pragma once
#include <pybind11/pybind11.h>
#include "opaque_types.h"

namespace py = pybind11;

void bind_aliases_module(py::module_&& m);
void bind_classes_module(py::module_&& m);
void bind_eigen_module(py::module_&& m);
void bind_enum_module(py::module_&& m);
void bind_flawed_bindings_module(py::module_&& m);
void bind_functions_module(py::module_&& m);
void bind_issues_module(py::module_&& m);
void bind_methods_module(py::module_&& m);
void bind_numpy_module(py::module_&& m);
void bind_properties_module(py::module_&& m);
void bind_stl_module(py::module_&& m);
void bind_stl_bind_module(py::module_&& m);
void bind_typing_module(py::module_&& m);
void bind_values_module(py::module_&& m);
