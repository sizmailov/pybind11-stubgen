#!/bin/bash

set -e

function parse_args() {

  CLEAR='\033[0m'
  RED='\033[0;31m'

  function usage() {
    if [ -n "$1" ]; then
      echo -e "${RED}👉 $1${CLEAR}\n";
    fi
    echo "Usage: $0 --stubs-sub-dir STUBS_SUB_DIR"
    echo "  --stubs-sub-dir       stubs output dir relative to this script directory"
    exit 1
  }

  # parse params
  while [[ "$#" > 0 ]]; do case $1 in
    --stubs-sub-dir) STUBS_SUB_DIR="$2";shift;shift;;
    *) usage "Unknown parameter passed: $1"; shift; shift;;
  esac; done

  # verify params
  if [ -z "$STUBS_SUB_DIR" ]; then usage "STUBS_SUB_DIR is not set"; fi;

  TESTS_ROOT="$(readlink -m "$(dirname "$0")")"
  STUBS_DIR=$(readlink -m "${TESTS_ROOT}/${STUBS_SUB_DIR}")
}

remove_stubs() {
    rm -rf "${STUBS_DIR}/*" ;
}

run_stubgen() {
  pybind11-stubgen \
      demo \
      --output-dir=${STUBS_DIR} \
      --numpy-array-wrap-with-annotated \
      --ignore-invalid-expressions="\(anonymous namespace\)::(Enum|Unbound)|<demo\._bindings\.flawed_bindings\..*" \
      --ignore-unresolved-names="typing\.Annotated" \
      --enum-class-locations="ConsoleForegroundColor:demo._bindings.enum" \
      --print-safe-value-reprs="Foo\(\d+\)" \
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
  (
    set -o pipefail ;
    git diff --exit-code HEAD -- "${STUBS_DIR}" | tee "${STUBS_DIR}.patch" ;
  )
}

main () {
  parse_args "$@"
  remove_stubs
  run_stubgen
  format_stubs
  check_stubs
}

main "$@"
