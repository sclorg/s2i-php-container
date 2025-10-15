import pytest

from container_ci_suite.helm import HelmChartsAPI

from conftest import VARS


class TestHelmRHELPHPImageStreams:

    def setup_method(self):
        package_name = "redhat-php-imagestreams"
        self.hc_api = HelmChartsAPI(
            path=VARS.TEST_DIR, package_name=package_name, tarball_dir=VARS.TEST_DIR, shared_cluster=True
        )
        self.hc_api.clone_helm_chart_repo(
            repo_url="https://github.com/sclorg/helm-charts", repo_name="helm-charts",
            subdir="charts/redhat"
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("8.3-ubi10", "registry.redhat.io/ubi10/php-83:latest", True),
            ("8.3-ubi9", "registry.redhat.io/ubi9/php-83:latest", True),
            ("8.2-ubi9", "registry.redhat.io/ubi9/php-82:latest", True),
            ("8.2-ubi8", "registry.redhat.io/ubi8/php-82:latest", True),
            ("8.1-ubi9", "registry.redhat.io/ubi9/php-81:latest", False),
            ("8.0-ubi9", "registry.redhat.io/ubi9/php-80:latest", True),
            ("8.0-ubi8", "registry.redhat.io/ubi8/php-80:latest", False),
            ("7.4-ubi8", "registry.redhat.io/ubi8/php-74:latest", True),
        ],
    )
    def test_package_imagestream(self, version, registry, expected):
        """
        Test checks if Helm imagestreams are present
        """
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry) == expected
