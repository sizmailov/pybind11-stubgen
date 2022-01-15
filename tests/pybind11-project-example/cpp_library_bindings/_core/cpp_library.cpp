#include "cpp_library/Foo.h"
#include "cpp_library/sublibA/add.h"
#include "cpp_library/sublibA/ConsoleColors.h"
#include "cpp_library/NestedClasses.h"
#include "cpp_library/Inheritance.h"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>


// namespace with types that lacks pybind counterpart
namespace forgotten {

struct Unbound {};

enum Enum{
    ONE=1,
    TWO=2
};

}


PYBIND11_MAKE_OPAQUE(std::map<std::string, std::complex<double>>);
PYBIND11_MAKE_OPAQUE(std::vector<std::pair<std::string, double>>);

namespace py = pybind11;

PYBIND11_MODULE(_core, m)
{
  auto pyFoo = py::class_<cpp_library::Foo>(m,"Foo");
  pyFoo
    .def(py::init<>())
    .def("f",&cpp_library::Foo::f);

  py::class_<cpp_library::Foo::Child> (pyFoo, "FooChild")
    .def(py::init<>())
    .def("g",&cpp_library::Foo::Child::g);

  auto sublibA = m.def_submodule("sublibA");
  sublibA.def("add", cpp_library::sublibA::add);

  py::enum_<cpp_library::sublibA::ConsoleForegroundColor> (sublibA, "ConsoleForegroundColor")
    .value("Green", cpp_library::sublibA::ConsoleForegroundColor::Green)
    .value("Yellow", cpp_library::sublibA::ConsoleForegroundColor::Yellow)
    .value("Blue", cpp_library::sublibA::ConsoleForegroundColor::Blue)
    .value("Magenta", cpp_library::sublibA::ConsoleForegroundColor::Magenta)
    .export_values();

  py::enum_<cpp_library::sublibA::ConsoleBackgroundColor> (sublibA, "ConsoleBackgroundColor")
    .value("Green", cpp_library::sublibA::Green)
    .value("Yellow", cpp_library::sublibA::Yellow)
    .value("Blue", cpp_library::sublibA::Blue)
    .value("Magenta", cpp_library::sublibA::Magenta)
    .export_values();

  sublibA.def("accept_defaulted_enum",
      [](const cpp_library::sublibA::ConsoleForegroundColor& color){},
      py::arg("color") = cpp_library::sublibA::ConsoleForegroundColor::Blue
  );


  auto pyOuter = py::class_<cpp_library::Outer> (m, "Outer");
  auto pyInner = py::class_<cpp_library::Outer::Inner> (pyOuter, "Inner");

  py::enum_<cpp_library::Outer::Inner::NestedEnum> (pyInner, "NestedEnum")
    .value("ONE", cpp_library::Outer::Inner::NestedEnum::ONE)
    .value("TWO", cpp_library::Outer::Inner::NestedEnum::TWO)
    ;

  py::class_<cpp_library::Base> pyBase(m, "Base");

  pyBase
    .def_readwrite("name", &cpp_library::Base::name);

  py::class_<cpp_library::Base::Inner>(pyBase, "Inner");

  py::class_<cpp_library::Derived, cpp_library::Base> (m, "Derived")
    .def_readwrite("count", &cpp_library::Derived::count);

  pyInner
    .def_readwrite("value", &cpp_library::Outer::Inner::value );

  pyOuter
    .def_readwrite("inner", &cpp_library::Outer::inner)
    .def_property_readonly_static("linalg", [](py::object){ return py::module::import("numpy.linalg"); });

  py::register_exception<cpp_library::CppException>(m, "CppException");

  m.attr("foovar") = cpp_library::Foo();

  py::list foolist;
  foolist.append(cpp_library::Foo());
  foolist.append(cpp_library::Foo());

  m.attr("foolist") = foolist;
  m.attr("none") = py::none();
  {
      py::list li;
      li.append(py::none{});
      li.append(2);
      li.append(py::dict{});
      m.attr("list_with_none") = li;
  }


  auto numeric = m.def_submodule("numeric");
  numeric.def("get_ndarray_int", []{ return py::array_t<int>{}; });
  numeric.def("get_ndarray_float64", []{ return py::array_t<double>{}; });
  numeric.def("accept_ndarray_int", [](py::array_t<int>){});
  numeric.def("accept_ndarray_float64", [](py::array_t<double>){});


  auto eigen = m.def_submodule("eigen");
  eigen.def("get_matrix_int", []{ return Eigen::Matrix3i{}; });
  eigen.def("get_vector_float64", []{ return Eigen::Vector3d{}; });
  eigen.def("accept_matrix_int", [](Eigen::Matrix3i){});
  eigen.def("accept_vector_float64", [](Eigen::Vector3d){});

  auto opaque_types = m.def_submodule("opaque_types");

  py::bind_vector<std::vector<std::pair<std::string, double>>>(opaque_types, "VectorPairStringDouble");
  py::bind_map<std::map<std::string, std::complex<double>>>(opaque_types, "MapStringComplex");

  opaque_types.def("get_complex_map", []{return std::map<std::string, std::complex<double>>{}; });
  opaque_types.def("get_vector_of_pairs", []{return std::vector<std::pair<std::string, double>>{}; });

  auto copy_types = m.def_submodule("copy_types");
  copy_types.def("get_complex_map", []{return std::map<int, std::complex<double>>{}; });
  copy_types.def("get_vector_of_pairs", []{return std::vector<std::pair<int, double>>{}; });

  // This submodule will have C++ signatures in python docstrings to emulate poorly written pybind11-bindings
  auto invalid_signatures = m.def_submodule("invalid_signatures");
  invalid_signatures.def("get_unbound_type", []{return forgotten::Unbound{}; });
  invalid_signatures.def("accept_unbound_type", [](std::pair<forgotten::Unbound, int>){ return 0;});
  invalid_signatures.def("accept_unbound_enum", [](forgotten::Enum){ return 0;});

  py::class_<forgotten::Unbound>(invalid_signatures, "Unbound");
  py::class_<forgotten::Enum>(invalid_signatures, "Enum");
  invalid_signatures.def("accept_unbound_type_defaulted", [](forgotten::Unbound){ return 0;}, py::arg("x")=forgotten::Unbound{});
  invalid_signatures.def("accept_unbound_enum_defaulted", [](forgotten::Enum){ return 0;}, py::arg("x")=forgotten::Enum::ONE);

  auto issues = m.def_submodule("issues");
  issues.def("issue_51", [](int*, int*){}, R"docstring(

    Use-case:
        issue_51(os.get_handle_inheritable, os.set_handle_inheritable))docstring");

  issues.def("issue_73_utf8_doc_chars", [] {}, py::doc(
      "Construct a Ramsete unicycle controller.\n"
      "\n"
      "Tuning parameter (b > 0 rad²/m²) for which larger values make\n"
      "\n"
      "convergence more aggressive like a proportional term.\n"
      "Tuning parameter (0 rad⁻¹ < zeta < 1 rad⁻¹) for which larger\n"
      "values provide more damping in response.")
  );
}