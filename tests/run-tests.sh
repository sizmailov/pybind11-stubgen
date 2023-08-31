#!/bin/bash

set -e

function parse_args() {

  CLEAR='\033[0m'
  RED='\033[0;31m'

  function usage() {
    if [ -n "$1" ]; then
      echo -e "${RED}👉 $1${CLEAR}\n";
    fi
    echo "Usage: $0 --pybind11-branch PYBIND11_BRANCH --stubs-sub-dir STUBS_SUB_DIR"
    echo "  --pybind11-branch     name of pybind11 branch"
    echo "  --stubs-sub-dir       stubs output dir relative to this script directory"
    exit 1
  }

  # parse params
  while [[ "$#" > 0 ]]; do case $1 in
    --pybind11-branch) PYBIND11_BRANCH="$2"; shift;shift;;
    --stubs-sub-dir) STUBS_SUB_DIR="$2";shift;shift;;
    *) usage "Unknown parameter passed: $1"; shift; shift;;
  esac; done

  # verify params
  if [ -z "$PYBIND11_BRANCH" ]; then usage "PYBIND11_BRANCH is not set"; fi;
  if [ -z "$STUBS_SUB_DIR" ]; then usage "STUBS_SUB_DIR is not set"; fi;

  TESTS_ROOT="$(dirname "$0")"
  PROJECT_ROOT="${TESTS_ROOT}/.."
  TEMP_DIR="${PROJECT_ROOT}/tmp/pybind11-${PYBIND11_BRANCH}"
  INSTALL_PREFIX="${TEMP_DIR}/install"
  BUILD_ROOT="${TEMP_DIR}/build"
  EXTERNAL_DIR="${TEMP_DIR}/external"
  STUBS_DIR="${TESTS_ROOT}/${STUBS_SUB_DIR}"
}


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
    rm -rf "${STUBS_DIR}/*" ;
}

run_stubgen() {
  pybind11-stubgen \
      demo \
      --output-dir=${STUBS_DIR} \
      --numpy-array-wrap-with-annotated-fixed-size \
      --ignore-invalid-expressions="\(anonymous namespace\)::(Enum|Unbound)" \
      --exit-code
}

format_stubs() {
  (
    cd "${STUBS_DIR}" ;
    black . ;
    isort --profile=black . ;
  )
}

check_stubs() {
  git add --all "${STUBS_DIR}" ;
  git diff --exit-code HEAD -- "${STUBS_DIR}"
}

main () {
  parse_args "$@"
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

main "$@"
