#!/bin/bash
#
# Functions for tests for the PHP image in OpenShift.
#
# IMAGE_NAME specifies a name of the candidate image used for testing.
# The image has to be available before this script is executed.
#

THISDIR=$(dirname ${BASH_SOURCE[0]})

source "${THISDIR}/test-lib.sh"
source "${THISDIR}/test-lib-openshift.sh"

function test_php_integration() {
  ct_os_test_s2i_app "${IMAGE_NAME}" \
                     "https://github.com/sclorg/s2i-php-container.git" \
                     "test/test-app" \
                     "Test PHP passed"
}

# Check the imagestream
function test_php_imagestream() {

  ct_os_test_image_stream_s2i "${THISDIR}/imagestreams/php-${OS%[0-9]*}.json" "${IMAGE_NAME}" \
                              "https://github.com/sclorg/s2i-php-container.git" \
                              test/test-app \
                              "Test PHP passed"
}

# Check the template
function test_php_template() {
  local supported_use_case
  if [ "${OS}" == "rhel8" ] && [ "${VERSION}" == "7.4" ]; then
    supported_use_case="True"
  fi
  if [ "${OS}" == "rhel7" ] && [ "${VERSION}" == "7.3" ]; then
    supported_use_case="True"
  fi
  if [ "${supported_use_case:-False}" == "True" ]; then
    BRANCH_TO_TEST="master"
    ct_os_test_template_app "${IMAGE_NAME}" \
                        https://raw.githubusercontent.com/sclorg/cakephp-ex/${BRANCH_TO_TEST}/openshift/templates/cakephp.json \
                        php \
                        'Welcome to your CakePHP application on OpenShift' \
                        8080 http 200 "-p SOURCE_REPOSITORY_REF=${BRANCH_TO_TEST} -p SOURCE_REPOSITORY_URL=https://github.com/sclorg/cakephp-ex.git -p PHP_VERSION=${VERSION} -p NAME=php-testing"
  fi
}

# vim: set tabstop=2:shiftwidth=2:expandtab:
