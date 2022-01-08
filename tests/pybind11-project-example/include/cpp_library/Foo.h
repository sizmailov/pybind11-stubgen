#pragma once
#include <stdexcept>

namespace cpp_library{


class CppException : public std::runtime_error {
  using std::runtime_error::runtime_error;
};

struct Foo {
    void f();

    struct Child {
        void g();
    };
};

}