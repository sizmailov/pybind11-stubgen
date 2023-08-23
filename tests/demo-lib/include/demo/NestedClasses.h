#pragma once

namespace demo{

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
