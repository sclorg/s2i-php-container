from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS


# Replacement with 'test_python_s2i_app_ex'
class TestS2IPHPTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix=f"php-{VARS.SHORT_VERSION}-testing", version=VARS.VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_php_template_inside_cluster(self):
        """
        Test checks if local repository with properly with `test/test-app`
        response is as expected
        """
        service_name = f"php-{VARS.SHORT_VERSION}-testing"
        assert self.oc_api.deploy_s2i_app(
            image_name=VARS.IMAGE_NAME, app="https://github.com/sclorg/s2i-php-container.git",
            context="test/test-app",
            service_name=service_name
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output="Test PHP passed"
        )
