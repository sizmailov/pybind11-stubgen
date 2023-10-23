#include "modules.h"

namespace {
struct Dummy {
    int regular_method(int x) { return x + 1; }
    static int static_method(int x) { return x + 1; }
};

} // namespace

void bind_methods_module(py::module&& m) {
    auto &&pyDummy = py::class_<Dummy>(m, "Dummy");

    pyDummy.def_static("def_static", &Dummy::static_method);
    pyDummy.def("def_", &Dummy::regular_method);
}
