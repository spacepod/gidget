#!/bin/bash
MAF_ROOT=${1:-/users/liype/maf_check_in}
export MAF_DATA_DIR=${MAF_ROOT}"/data"
export MAF_REFERENCES_DIR=${MAF_ROOT}"/reference"
export MAF_TOOLS_DIR=${MAF_ROOT}"/tools"
export MAF_SCRIPTS_DIR=${MAF_ROOT}"/src"
export MAF_PYTHON_BINARY="/tools/bin/python2.7"