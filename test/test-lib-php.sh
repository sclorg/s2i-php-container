#!/bin/bash
#
# Functions for tests for the PHP image in OpenShift.
#
# IMAGE_NAME specifies a name of the candidate image used for testing.
# The image has to be available before this script is executed.
#

THISDIR=$(dirname ${BASH_SOURCE[0]})

source ${THISDIR}/test-lib.sh
source ${THISDIR}/test-lib-openshift.sh

function test_php_integration() {
  local image_name=$1
  local version=$2
  local import_image=$3
  VERSION=$version ct_os_test_s2i_app "${image_name}" \
                                      "https://github.com/sclorg/s2i-php-container.git" \
                                      test/test-app \
                                      "Test PHP passed" \
                                      8080 http 200
}

# Check the imagestream
function test_php_imagestream() {
  case ${OS} in
    rhel7|centos7) ;;
    *) echo "Imagestream testing not supported for $OS environment." ; return 0 ;;
  esac

  ct_os_test_image_stream_s2i "${THISDIR}/imagestreams/php-${OS}.json" "${IMAGE_NAME}" \
                              "https://github.com/sclorg/s2i-php-container.git" \
                              test/test-app \
                              "Test PHP passed"
}

# vim: set tabstop=2:shiftwidth=2:expandtab:
