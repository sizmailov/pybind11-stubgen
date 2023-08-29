cmake_minimum_required(VERSION 3.12)
project(demo
        LANGUAGES
        CXX
        VERSION
        1.0
)

find_package(Eigen3 REQUIRED CONFIG)

file(GLOB_RECURSE DEMO_SOURCES ./src/**.cpp ./src/**.h)
add_library(demo STATIC ${DEMO_SOURCES})
target_include_directories(demo PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)
target_include_directories(demo PRIVATE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
)
target_link_libraries(demo PUBLIC Eigen3::Eigen)
set_property(TARGET demo PROPERTY POSITION_INDEPENDENT_CODE ON)

add_library(Demo::demo ALIAS demo)

include(GNUInstallDirs)

install(TARGETS demo EXPORT DemoTargets
        PUBLIC_HEADER DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/demo"
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/include/" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
set(DEMO_CMAKECONFIG_INSTALL_DIR
        "${CMAKE_INSTALL_DATAROOTDIR}/cmake/${PROJECT_NAME}"
        CACHE STRING "install path for DemoConfig.cmake")
install(EXPORT DemoTargets NAMESPACE Demo:: DESTINATION ${DEMO_CMAKECONFIG_INSTALL_DIR})

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
        DemoConfigVersion.cmake
        VERSION ${PACKAGE_VERSION}
        COMPATIBILITY SameMajorVersion
)

install(
        FILES
        ./DemoConfig.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/DemoConfigVersion.cmake
        DESTINATION
        ${DEMO_CMAKECONFIG_INSTALL_DIR}
)
