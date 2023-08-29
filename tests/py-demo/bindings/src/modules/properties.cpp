#include "modules.h"

namespace {
struct Dummy {
    int value;
    static int static_value;
};

} // namespace

int Dummy::static_value = 0;

void bind_properties_module(py::module_&& m) {

    auto &&pyDummy = py::class_<Dummy>(m, "Dummy");

    pyDummy.def_readwrite("def_readwrite", &Dummy::value);
    pyDummy.def_property(
        "def_property",
        [](Dummy &self) { return self.value; },
        [](Dummy self, int value) { self.value = value; });
    pyDummy.def_property_readonly("def_property_readonly", [](Dummy &self) { return self.value; });
    pyDummy.def_readonly("def_readonly", &Dummy::value);
    pyDummy.def_property_static(
        "def_property_static",
        [](py::object & /* self */) { return Dummy::static_value; },
        [](py::object & /* self */, int value) { Dummy::static_value = value; });
    pyDummy.def_property_readonly_static(
        "def_property_readonly_static",
        [](py::object & /* self */) { return Dummy::static_value; });
}
