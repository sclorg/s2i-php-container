import os
import sys

import pytest
from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")

if VERSION == "7.4" or VERSION == "8.0":
    branch_to_test = "4.X"
    check_msg = "Welcome to CakePHP 4.5"
elif VERSION == "8.1" or VERSION == "8.2" or VERSION == "8.3":
    branch_to_test = "5.X"
    check_msg = "Welcome to CakePHP 5"
else:
    branch_to_test = "master"
    check_msg = "Welcome to your CakePHP application on OpenShift"

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9"
}
TAG = TAGS.get(OS, None)

DEPLOYED_MYSQL_IMAGE = "quay.io/sclorg/mysql-80-c8s"
IMAGE_SHORT = f"mysql:8.0-el8"
IMAGE_TAG = f"8.0-el8"


class TestDeployTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="php-testing", version=VERSION)
        self.oc_api.import_is("imagestreams/php-rhel.json", "", skip_check=True)
        assert self.oc_api.upload_image(DEPLOYED_MYSQL_IMAGE, IMAGE_SHORT)

    def teardown_method(self):
        self.oc_api.delete_project()

    @pytest.mark.parametrize(
        "template",
        [
            "cakephp.json",
        ]
    )
    def test_php_template_inside_cluster(self, template):

        service_name = "php-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="cakephp-ex", dir="openshift/templates", filename=template, branch=branch_to_test
        )
        openshift_args = [
            f"SOURCE_REPOSITORY_REF={branch_to_test}",
            f"PHP_VERSION={VERSION}{TAG}",
            f"NAME={service_name}"
        ]
        if template != "cakephp.json":
            openshift_args.extend([
                f"MYSQL_VERSION={IMAGE_TAG}",
                f"DATABASE_USER=testu",
                f"DATABASE_PASSWORD=testp"
            ])
        assert self.oc_api.deploy_template_with_image(
            image_name=IMAGE_NAME,
            template=template_url,
            name_in_template="php",
            openshift_args=openshift_args
        )
        assert self.oc_api.template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output=check_msg
        )
