from container_ci_suite.helm import HelmChartsAPI

from conftest import VARS, TAGS


class TestHelmCakePHPTemplate:

    def setup_method(self):
        package_name = "redhat-cakephp-application-template"
        self.hc_api = HelmChartsAPI(path=VARS.TEST_DIR, package_name=package_name, tarball_dir=VARS.TEST_DIR)
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_by_helm_test(self):
        self.hc_api.package_name = "redhat-php-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-cakephp-application-template"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "php_version": f"{VARS.VERSION}{TAGS.get(VARS.OS)}",
                "namespace": self.hc_api.namespace,
                "source_repository_ref": VARS.BRANCH_TO_TEST,
                "name": "cakephp-example"
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="cakephp-example", timeout=480)
        assert self.hc_api.test_helm_chart(expected_str=[VARS.CHECK_MSG])
