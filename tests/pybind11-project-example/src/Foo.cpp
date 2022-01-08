#include "cpp_library/Foo.h"

#include <iostream>

void cpp_library::Foo::f() {
    std::cout << "invoked cpp_library::Foo::f()" << std::endl;
}

void cpp_library::Foo::Child::g() {
    std::cout << "invoked cpp_library::Foo::Child::g()" << std::endl;
}
