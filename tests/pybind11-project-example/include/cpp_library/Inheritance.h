#pragma once
#include <string>

namespace cpp_library{

struct Base {
  struct Inner{};
  std::string name;
};

struct Derived : Base {
  int count;
};

}