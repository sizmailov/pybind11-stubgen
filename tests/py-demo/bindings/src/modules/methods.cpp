#include "modules.h"

namespace mymodules {
struct Dummy {
    int regular_method(int x) { return x + 1; }
    static int static_method(int x) { return x + 1; }
};

} // namespace

void bind_methods_module(py::module&& m) {
    auto &&pyDummy = py::class_<mymodules::Dummy>(m, "Dummy");

    pyDummy.def_static("static_method", &mymodules::Dummy::static_method);
    pyDummy.def("regular_method", &mymodules::Dummy::regular_method);
}
