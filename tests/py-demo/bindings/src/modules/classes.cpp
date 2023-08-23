#include "modules.h"

#include <demo/Foo.h>
#include <demo/Inheritance.h>
#include <demo/NestedClasses.h>

void bind_classes_module(py::module_&&m) {

    {
        auto pyOuter = py::class_<demo::Outer>(m, "Outer");
        auto pyInner = py::class_<demo::Outer::Inner>(pyOuter, "Inner");

        py::enum_<demo::Outer::Inner::NestedEnum>(pyInner, "NestedEnum")
            .value("ONE", demo::Outer::Inner::NestedEnum::ONE)
            .value("TWO", demo::Outer::Inner::NestedEnum::TWO);

        pyInner.def_readwrite("value", &demo::Outer::Inner::value);
        pyOuter.def_readwrite("inner", &demo::Outer::inner);
    }

    {
        py::class_<demo::Base> pyBase(m, "Base");

        pyBase.def_readwrite("name", &demo::Base::name);

        py::class_<demo::Base::Inner>(pyBase, "Inner");

        py::class_<demo::Derived, demo::Base>(m, "Derived")
            .def_readwrite("count", &demo::Derived::count);

    }
    {
        auto pyFoo = py::class_<demo::Foo>(m, "Foo");
        pyFoo.def(py::init<>()).def("f", &demo::Foo::f);

        py::class_<demo::Foo::Child>(pyFoo, "FooChild")
            .def(py::init<>())
            .def("g", &demo::Foo::Child::g);
    }

    {
        py::register_exception<demo::CppException>(m, "CppException");
    }
}
