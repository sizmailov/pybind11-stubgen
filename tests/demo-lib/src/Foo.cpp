#include "demo/Foo.h"

#include <iostream>

void demo::Foo::f() {
    std::cout << "invoked demo::Foo::f()" << std::endl;
}

void demo::Foo::Child::g() {
    std::cout << "invoked demo::Foo::Child::g()" << std::endl;
}
