# shellcheck shell=bash
# some functions are used from test-lib.sh, that is usually in the same dir
# shellcheck source=/dev/null
source "$(dirname "${BASH_SOURCE[0]}")"/test-lib.sh

# Set of functions for testing docker images in OpenShift using 'oc' command

# A variable containing the overall test result; must be changed to 0 in the end
# of the testing script:
#   OS_TESTSUITE_RESULT=0
# And the following trap must be set, in the beginning of the test script:
#   trap ct_os_cleanup EXIT SIGINT

# ct_os_set_path_oc_4 OC_VERSION
# --------------------
# This is a trick that helps using correct version 4 of the `oc`:
# The input is version of the openshift in format 4.4 etc.
# If the currently available version of oc is not of this version,
# it first takes a look into /usr/local/oc-<ver>/bin directory,

# Arguments: oc_version - X.Y part of the version of OSE (e.g. 3.9)
function ct_os_set_path_oc_4() {
    echo "Setting OCP4 client"
    local oc_version=$1
    local installed_oc_path="/usr/local/oc-v${oc_version}/bin"
    echo "PATH ${installed_oc_path}"
    if [ -x "${installed_oc_path}/oc" ] ; then
        oc_path="${installed_oc_path}"
        echo "Binary oc found in ${installed_oc_path}" >&2
    else
       echo "OCP4 not found"
       return 1
    fi
    export PATH="${oc_path}:${PATH}"
    oc version
    if ! oc version | grep -q "Client Version: ${oc_version}." ; then
        echo "ERROR: something went wrong, oc located at ${oc_path}, but oc of version ${oc_version} not found in PATH ($PATH)" >&1
        return 1
    else
        echo "PATH set correctly, binary oc found in version ${oc_version}: $(command -v oc)"
    fi
}

# ct_os_prepare_ocp4
# ------------------
# Prepares environment for testing images in OpenShift 4 environment
#
#
function ct_os_set_ocp4() {
  if [ "${CVP:-0}" -eq "1" ]; then
    echo "Testing in CVP environment. No need to login to OpenShift cluster. This is already done by CVP pipeline."
    return
  fi
  local login
  OS_OC_CLIENT_VERSION=${OS_OC_CLIENT_VERSION:-4.4}
  ct_os_set_path_oc_4 "${OS_OC_CLIENT_VERSION}"

  oc version

  login=$(cat "$KUBEPASSWORD")
  oc login -u kubeadmin -p "$login"
  echo "Login to OpenShift ${OS_OC_CLIENT_VERSION} is DONE"
  # let openshift cluster to sync to avoid some race condition errors
  sleep 3
}

function ct_os_upload_image_external_registry() {
  local input_name="${1}" ; shift
  local image_name=${input_name##*/}
  local imagestream=${1:-$image_name:latest}
  local output_name

  ct_os_login_external_registry

  output_name="${INTERNAL_DOCKER_REGISTRY}/rhscl-ci-testing/$imagestream"

  docker images
  docker tag "${input_name}" "${output_name}"
  docker push "${output_name}"
}


function ct_os_login_external_registry() {
  local docker_token
  # docker login fails with "404 page not found" error sometimes, just try it more times
  # shellcheck disable=SC2034
  echo "loging"
  [ -z "${INTERNAL_DOCKER_REGISTRY:-}" ] && "INTERNAL_DOCKER_REGISTRY has to be set for working with Internal registry" && return 1
  # shellcheck disable=SC2034
  for i in $(seq 12) ; do
    # shellcheck disable=SC2015
    docker_token=$(cat "$DOCKER_UPSHIFT_TOKEN")
    # shellcheck disable=SC2015
    docker login -u rhscl-ci-testing -p "$docker_token" "${INTERNAL_DOCKER_REGISTRY}" && return 0 || :
    sleep 5
  done
  return 1
}

function ct_os_import_image_ocp4() {
  local image_name="${1}"; shift
  local imagestream=${1:-$image_name:latest}
  local namespace

  namespace=${CT_NAMESPACE:-"$(oc project -q)"}
  deploy_image_name="${INTERNAL_DOCKER_REGISTRY}/rhscl-ci-testing/${imagestream}"
  echo "Uploading image ${image_name} as ${deploy_image_name} , ${imagestream} into external registry."
  ct_os_upload_image_external_registry "${image_name}" "${imagestream}"
  if [ "${CT_TAG_IMAGE:-false}" == 'true' ]; then
    echo "Tag ${deploy_image_name} to ${namespace}/${imagestream}"
    oc tag --source=docker "${deploy_image_name}" "${namespace}/${imagestream}" --insecure=true --reference-policy=local
  else
    echo "Import image into OpenShift 4 environment ${namespace}/${imagestream} from ${deploy_image_name}"
    oc import-image "${namespace}/${imagestream}" --from="${deploy_image_name}" --confirm --reference-policy=local
  fi
}
