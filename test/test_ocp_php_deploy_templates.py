import pytest
from container_ci_suite.openshift import OpenShiftAPI

from conftest import VARS


class TestDeployTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix=f"php-{VARS.SHORT_VERSION}-testing", version=VARS.VERSION)

    def teardown_method(self):
        self.oc_api.delete_project()

    @pytest.mark.parametrize(
        "template",
        [
            "cakephp.json",
        ]
    )
    def test_php_template_inside_cluster(self, template):
        """
        Test checks if local imagestreams and example application `cakephp-ex` works with properly
        and response is as expected
        """
        self.oc_api.import_is("imagestreams/php-rhel.json", "", skip_check=True)
        service_name = f"php-{VARS.SHORT_VERSION}-testing"
        template_url = self.oc_api.get_raw_url_for_json(
            container="cakephp-ex", dir="openshift/templates", filename=template, branch=VARS.BRANCH_TO_TEST
        )
        openshift_args = [
            f"SOURCE_REPOSITORY_REF={VARS.BRANCH_TO_TEST}",
            f"PHP_VERSION={VARS.SHORT_VERSION}{VARS.TAG}",
            f"NAME={service_name}"
        ]
        # if template != "cakephp.json":
        #     openshift_args.extend([
        #         f"MYSQL_VERSION={IMAGE_TAG}",
        #         f"DATABASE_USER=testu",
        #         f"DATABASE_PASSWORD=testp"
        #     ])
        assert self.oc_api.deploy_template_with_image(
            image_name=VARS.IMAGE_NAME,
            template=template_url,
            name_in_template="php",
            openshift_args=openshift_args
        )
        assert self.oc_api.is_template_deployed(name_in_template=service_name)
        assert self.oc_api.check_response_inside_cluster(
            name_in_template=service_name, expected_output=VARS.CHECK_MSG
        )
