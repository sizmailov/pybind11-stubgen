#pragma once

namespace cpp_library{

struct Outer {

  struct Inner{

    enum class NestedEnum {
      ONE=1,
      TWO
    };

    NestedEnum value;
  };

  Inner inner;
};

}