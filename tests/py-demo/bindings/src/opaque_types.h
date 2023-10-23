#pragma once

#include <complex>
#include <map>
#include <vector>

using MapStringComplex = std::map<std::string, std::complex<double>>;
using VectorPairStringDouble = std::vector<std::pair<std::string, double>>;
PYBIND11_MAKE_OPAQUE(MapStringComplex);
PYBIND11_MAKE_OPAQUE(VectorPairStringDouble);
