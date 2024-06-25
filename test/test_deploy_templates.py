import os
import sys

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, SINGLE_VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("SINGLE_VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")

if VERSION == "7.4" or VERSION == "8.0":
    branch_to_test = "4.X"
    check_msg = "Welcome to CakePHP 4.5"
elif VERSION == "8.1" or VERSION == "8.2":
    branch_to_test = "5.X"
    check_msg = "Welcome to CakePHP 5"
else:
    branch_to_test = "master"
    check_msg = "Welcome to your CakePHP application on OpenShift"


class TestDeployTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="php-testing", version=VERSION)
        self.oc_api.import_is("imagestreams/php-rhel.json", "", skip_check=True)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_php_template_inside_cluster(self):

        service_name = "php-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="cakephp-ex", dir="openshift/templates", filename="cakephp.json", branch=branch_to_test
        )
        assert self.oc_api.deploy_template_with_image(
            image_name=IMAGE_NAME,
            template=template_url,
            name_in_template="php",
            openshift_args=[
                f"SOURCE_REPOSITORY_REF={branch_to_test}",
                f"PHP_VERSION={VERSION}",
                f"SOURCE_REPOSITORY_URL=https://github.com/sclorg/cakephp-ex.git",
                f"NAME={service_name}"
            ]
        )
        assert self.oc_api.template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output=check_msg
        )
