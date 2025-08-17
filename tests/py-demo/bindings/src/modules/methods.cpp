#include "modules.h"

namespace {
struct Dummy {
    int regular_method(int x) { return x + 1; }
    static int static_method(int x) { return x + 1; }
};

} // namespace

void bind_methods_module(py::module&& m) {
    auto &&pyDummy = py::class_<Dummy>(m, "Dummy");

    pyDummy.def_static("static_method", &Dummy::static_method);
    pyDummy.def("regular_method", &Dummy::regular_method);
}
