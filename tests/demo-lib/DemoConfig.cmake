include(CMakeFindDependencyMacro)
find_dependency(Eigen3 REQUIRED)

include("${CMAKE_CURRENT_LIST_DIR}/DemoTargets.cmake")
