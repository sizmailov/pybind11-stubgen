#pragma once
#include <string>

namespace demo{

struct Base {
  struct Inner{};
  std::string name;
};

struct Derived : Base {
  int count;
};

}
