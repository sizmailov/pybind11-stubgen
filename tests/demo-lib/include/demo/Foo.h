#pragma once
#include <stdexcept>

namespace demo{


class CppException : public std::runtime_error {
  //using std::runtime_error;
};

struct Foo {
    void f();

    struct Child {
        void g();
    };
};

}
