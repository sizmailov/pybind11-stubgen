file(GLOB_RECURSE PYXMOLPP_SOURCES
        _core/**.cpp
        _core/**.h
)
pybind11_add_module(_core ${PYXMOLPP_SOURCES})
target_include_directories(_core PRIVATE ${CMAKE_CURRENT_LIST_DIR}/_core)
target_link_libraries(_core PRIVATE cpp_library)