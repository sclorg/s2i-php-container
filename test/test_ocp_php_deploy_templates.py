from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS, skip_clear_env_tests


class TestDeployTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix=f"php-{VARS.SHORT_VERSION}-testing", version=VARS.VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_php_template_inside_cluster(self):
        """
        Test checks if local imagestreams and example application `cakephp-ex` works with properly
        and response is as expected
        """
        skip_clear_env_tests()
        self.oc_api.import_is("imagestreams/php-rhel.json", "", skip_check=True)
        service_name = f"php-{VARS.SHORT_VERSION}-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="cakephp-ex", dir="openshift/templates", filename="cakephp.json", branch=VARS.BRANCH_TO_TEST
        )
        openshift_args = [
            f"SOURCE_REPOSITORY_REF={VARS.BRANCH_TO_TEST}",
            "SOURCE_REPOSITORY_URL=https://github.com/sclorg/cakephp-ex.git",
            f"PHP_VERSION={VARS.VERSION}{VARS.TAG}",
            f"NAME={service_name}"
        ]
        assert self.oc_api.deploy_template_with_image(
            image_name=VARS.IMAGE_NAME,
            template=template_url,
            name_in_template="php",
            openshift_args=openshift_args
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name, timeout=480)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output=VARS.CHECK_MSG
        )
