import os
import sys

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI
from container_ci_suite.utils import check_variables

if not check_variables():
    print("At least one variable from IMAGE_NAME, OS, VERSION is missing.")
    sys.exit(1)


test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


VERSION = os.getenv("VERSION")
IMAGE_NAME = os.getenv("IMAGE_NAME")
OS = os.getenv("TARGET")

if VERSION == "7.4" or VERSION == "8.0":
    check_msg = "Welcome to CakePHP"
elif VERSION == "8.1" or VERSION == "8.2" or VERSION == "8.3":
    check_msg = "Welcome to CakePHP"
else:
    check_msg = "Welcome to your CakePHP application on OpenShift"

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9"
}
TAG = TAGS.get(OS, None)


class TestHelmCakePHPTemplate:

    def setup_method(self):
        package_name = "redhat-php-cakephp-application"
        path = test_dir
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_curl_connection(self):
        if OS == "rhel10":
            pytest.skip("Do NOT test on RHEL10 yet.")
        if VERSION == "8.3":
            pytest.skip("Do NOT test on version 8.3 yet.")

        branch_to_test = "4.X"
        check_msg = "Welcome to CakePHP"
        if self.hc_api.shared_cluster:
            pytest.skip("Do NOT test on shared cluster")
        if VERSION.startswith("8.2") or VERSION.startswith("8.3"):
            branch_to_test = "5.X"
            check_msg = "Welcome to CakePHP"
        self.hc_api.package_name = "redhat-php-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-php-cakephp-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "php_version": f"{VERSION}{TAG}",
                "namespace": self.hc_api.namespace,
                "source_repository_ref": branch_to_test,
                "name": "cakephp-example"
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="cakephp-example", timeout=480)
        assert self.hc_api.oc_api.check_response_inside_cluster(
            name_in_template="cakephp-example",
            expected_output=check_msg,
        )

    def test_by_helm_test(self):
        if OS == "rhel10":
            pytest.skip("Do NOT test on RHEL10 yet.")
        if VERSION == "8.3":
            pytest.skip("Do NOT test on version 8.3 yet.")
        branch_to_test = "4.X"
        check_msg = "Welcome to CakePHP"
        if VERSION.startswith("8.2") or VERSION.startswith("8.3"):
            branch_to_test = "5.X"
            check_msg = "Welcome to CakePHP"
        self.hc_api.package_name = "redhat-php-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-php-cakephp-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "php_version": f"{VERSION}{TAG}",
                "namespace": self.hc_api.namespace,
                "source_repository_ref": branch_to_test,
                "name": "cakephp-example"
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="cakephp-example", timeout=480)
        assert self.hc_api.test_helm_chart(expected_str=[check_msg])
