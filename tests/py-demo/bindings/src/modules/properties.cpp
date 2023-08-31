#include "modules.h"

namespace {
struct WithoutDoc {
    int value;
    static int static_value;
};

struct WithPropDoc {
    int value;
    static int static_value;
};

struct WithGetterSetterDoc {
    int value;
    static int static_value;
};

struct WithPropAndGetterSetterDoc {
    int value;
    static int static_value;
};

} // namespace

int WithoutDoc::static_value = 0;
int WithPropDoc::static_value = 0;
int WithGetterSetterDoc::static_value = 0;
int WithPropAndGetterSetterDoc::static_value = 0;

void bind_properties_module(py::module_ &&m) {
    {
        auto &&pyDummy = py::class_<WithoutDoc>(m, "WithoutDoc", "No user docstring provided");

        pyDummy.def_readwrite("def_readwrite", &WithoutDoc::value);
        pyDummy.def_property(
            "def_property",
            [](WithoutDoc &self) { return self.value; },
            [](WithoutDoc self, int value) { self.value = value; });
        pyDummy.def_property_readonly("def_property_readonly",
                                      [](WithoutDoc &self) { return self.value; });
        pyDummy.def_readonly("def_readonly", &WithoutDoc::value);
        pyDummy.def_property_static(
            "def_property_static",
            [](py::object & /* self */) { return WithoutDoc::static_value; },
            [](py::object & /* self */, int value) { WithoutDoc::static_value = value; });
        pyDummy.def_property_readonly_static(
            "def_property_readonly_static",
            [](py::object & /* self */) { return WithoutDoc::static_value; });
    }

    {
        auto &&pyDummy = py::class_<WithPropDoc>(
            m, "WithPropDoc", "User docstring provided only to `def_` calls");

        auto &&doc = py::doc("prop doc token");
        pyDummy.def_readwrite("def_readwrite", &WithPropDoc::value, doc);
        pyDummy.def_property(
            "def_property",
            [](WithPropDoc &self) { return self.value; },
            [](WithPropDoc self, int value) { self.value = value; },
            doc);
        pyDummy.def_property_readonly(
            "def_property_readonly", [](WithPropDoc &self) { return self.value; }, doc);
        pyDummy.def_readonly("def_readonly", &WithPropDoc::value, doc);
        pyDummy.def_property_static(
            "def_property_static",
            [](py::object & /* self */) { return WithPropDoc::static_value; },
            [](py::object & /* self */, int value) { WithPropDoc::static_value = value; },
            doc);
        pyDummy.def_property_readonly_static(
            "def_property_readonly_static",
            [](py::object & /* self */) { return WithPropDoc::static_value; },
            doc);
    }

    {
        auto &&pyDummy = py::class_<WithGetterSetterDoc>(
            m,
            "WithGetterSetterDoc",
            "User docstring provided via pybind11::cpp_function(..., doc) to getters/setters, but "
            "NOT to `def_*(..., doc)` calls");

        auto &&getter_doc = py::doc("getter doc token");
        auto &&setter_doc = py::doc("setter doc token");
        pyDummy.def_property(
            "def_property",
            py::cpp_function([](WithGetterSetterDoc &self) { return self.value; }, getter_doc),
            py::cpp_function([](WithGetterSetterDoc self, int value) { self.value = value; },
                             setter_doc));
        pyDummy.def_property_readonly(
            "def_property_readonly",
            py::cpp_function([](WithGetterSetterDoc &self) { return self.value; }, getter_doc));
        pyDummy.def_property_static(
            "def_property_static",
            py::cpp_function(
                [](py::object & /* self */) { return WithGetterSetterDoc::static_value; },
                getter_doc),
            py::cpp_function([](py::object & /* self */,
                                int value) { WithGetterSetterDoc::static_value = value; },
                             setter_doc));
        pyDummy.def_property_readonly_static("def_property_readonly_static",
                                             py::cpp_function([](py::object & /* self */) {
                                                 return WithGetterSetterDoc::static_value;
                                             }),
                                             getter_doc);
    }

    {
        auto &&pyDummy = py::class_<WithPropAndGetterSetterDoc>(
            m,
            "WithPropAndGetterSetterDoc",
            "User docstring provided via pybind11::cpp_function(..., doc) to getters/setters and "
            "to `def_*(, doc)` calls");

        auto &&prop_doc = py::doc("prop doc token");
        auto &&getter_doc = py::doc("getter doc token");
        auto &&setter_doc = py::doc("setter doc token");
        pyDummy.def_property(
            "def_property",
            py::cpp_function([](WithPropAndGetterSetterDoc &self) { return self.value; },
                             getter_doc),
            py::cpp_function(
                [](WithPropAndGetterSetterDoc self, int value) { self.value = value; },
                setter_doc),
            prop_doc);
        pyDummy.def_property_readonly(
            "def_property_readonly",
            py::cpp_function([](WithPropAndGetterSetterDoc &self) { return self.value; },
                             getter_doc),
            prop_doc);
        pyDummy.def_property_static(
            "def_property_static",
            py::cpp_function(
                [](py::object & /* self */) { return WithPropAndGetterSetterDoc::static_value; },
                getter_doc),
            py::cpp_function([](py::object & /* self */,
                                int value) { WithPropAndGetterSetterDoc::static_value = value; },
                             setter_doc),
            prop_doc);
        pyDummy.def_property_readonly_static(
            "def_property_readonly_static",
            py::cpp_function(
                [](py::object & /* self */) { return WithPropAndGetterSetterDoc::static_value; },
                getter_doc),
            prop_doc);
    }
}
