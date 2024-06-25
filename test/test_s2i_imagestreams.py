import os
import sys

from container_ci_suite.openshift import OpenShiftAPI
from container_ci_suite.utils import check_variables


if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, SINGLE_VERSION is missing.")
    sys.exit(1)


VERSION = os.getenv("SINGLE_VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("OS")

SHORT_VERSION = "".join(VERSION.split("."))


class TestPHPImagestreams:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="php", version=VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_php_template_inside_cluster(self):
        service_name = f"php-{SHORT_VERSION}-testing"
        assert self.oc_api.deploy_imagestream_s2i(
            imagestream_file="imagestreams/php-rhel.json",
            image_name=IMAGE_NAME,
            app="https://github.com/sclorg/s2i-php-container.git",
            context="test/test-app"
        )
        assert self.oc_api.template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Test PHP passed"
        )
