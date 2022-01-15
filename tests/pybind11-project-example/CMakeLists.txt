cmake_minimum_required(VERSION 3.8)
project(pybind11_project_example)

set(CMAKE_CXX_STANDARD 11)


find_package(PythonInterp REQUIRED)
find_package(PythonLibs "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}" REQUIRED )
if (PYTHONLIBS_FOUND)
    include_directories(${PYTHON_INCLUDE_DIRS})
    message("Using default python version: " ${PYTHONLIBS_VERSION_STRING})
endif()


add_subdirectory(external/pybind11)
include_directories(SYSTEM external/pybind11/include)
include_directories(SYSTEM external/eigen)

file(GLOB_RECURSE SOURCES src/**.cpp)
add_library(cpp_library STATIC ${SOURCES})
set_property(TARGET cpp_library PROPERTY POSITION_INDEPENDENT_CODE ON)
target_include_directories(cpp_library PUBLIC ./include)

add_subdirectory(cpp_library_bindings)