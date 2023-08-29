#!/bin/bash

set -e

PYBIND11_BRANCH="v2.11"
TESTS_ROOT="$(dirname "$0")"
PROJECT_ROOT="${TESTS_ROOT}/.."
TEMP_DIR="${PROJECT_ROOT}/tmp/pybind-${PYBIND11_BRANCH}"
INSTALL_PREFIX="${TEMP_DIR}/install"
BUILD_ROOT="${TEMP_DIR}/build"
EXTERNAL_DIR="${TEMP_DIR}/external"


clone_eigen() {
  mkdir -p "${EXTERNAL_DIR}"
  if [ ! -d "${EXTERNAL_DIR}/eigen" ]; then
    git clone \
        --depth 1 \
        --branch master \
        --single-branch \
        https://gitlab.com/libeigen/eigen.git \
        "${EXTERNAL_DIR}/eigen"
  fi
}

clone_pybind11() {
  mkdir -p "${EXTERNAL_DIR}"
  if [ ! -d "${EXTERNAL_DIR}/pybind11" ]; then
    git clone \
        --depth 1 \
        --branch "${PYBIND11_BRANCH}" \
        --single-branch \
        https://github.com/pybind/pybind11.git \
        "${EXTERNAL_DIR}/pybind11"
  fi
}

install_eigen() {
  cmake -S "${EXTERNAL_DIR}/eigen" -B "${BUILD_ROOT}/eigen"
  cmake --install "${BUILD_ROOT}/eigen" \
        --prefix "${INSTALL_PREFIX}"
}

install_pybind11() {
  cmake -S "${EXTERNAL_DIR}/pybind11" -B "${BUILD_ROOT}/pybind11"
  cmake --install "${BUILD_ROOT}/pybind11" \
        --prefix "${INSTALL_PREFIX}"
}

install_demo() {
  cmake -S "${TESTS_ROOT}/demo-lib" -B "${BUILD_ROOT}/demo"
  cmake --build "${BUILD_ROOT}/demo"
  cmake --install "${BUILD_ROOT}/demo" \
        --prefix "${INSTALL_PREFIX}"
}

install_pydemo() {
  (
    export CMAKE_PREFIX_PATH="$(readlink -m "${INSTALL_PREFIX}")";
    pip install "${TESTS_ROOT}/py-demo"
  )
}

remove_stubs() {
    rm -rf "${TESTS_ROOT}/stubs" ;
}

run_stubgen() {
  pybind11-stubgen \
      demo \
      --output-dir="${TESTS_ROOT}/stubs" \
      --numpy-array-wrap-with-annotated-fixed-size \
      --ignore-all-errors
}

format_stubs() {
  (
    cd "${TESTS_ROOT}/stubs" ;
    black . ;
    isort --profile=black . ;
  )
}

check_stubs() {
  git add --all "${TESTS_ROOT}/stubs" ;
  git diff --exit-code HEAD -- "${TESTS_ROOT}/stubs"
}

main () {
  clone_eigen
  clone_pybind11
  install_pybind11
  install_eigen
  install_demo
  install_pydemo
  remove_stubs
  run_stubgen
  format_stubs
  check_stubs
}

main
