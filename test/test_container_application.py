import re

import pytest

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.podman_wrapper import PodmanCLIWrapper
from container_ci_suite.engines.container import ContainerImage

from conftest import VARS, skip_clear_env_tests

test_app = VARS.TEST_DIR / "test-app"


def build_npm_app(app_path: Path) -> ContainerTestLib:
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args=f"--pull-policy=never {container_lib.build_s2i_npm_variables()}",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-testapp"
    )
    return s2i_app


def build_s2i_app(app_path: Path, container_args: str = "") -> ContainerTestLib:
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    app_name = app_path.name
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args=f"--pull-policy=never {container_args} {container_lib.build_s2i_npm_variables()}",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-{app_name}"
    )
    return s2i_app


class TestPHPTestApplicationContainer:
    def setup_method(self):
        self.s2i_app = build_s2i_app(test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_run_s2i_usage(self):
        output = self.s2i_app.s2i_usage()
        assert output

    def test_docker_run_usage(self):
        assert PodmanCLIWrapper.call_podman_command(
            cmd=f"run --rm {VARS.IMAGE_NAME} &>/dev/null",
            return_output=False
        ) == 0

    @pytest.mark.parametrize(
        "container_arg",
        [
            "",
            "-u 12345",
        ]
    )
    def test_run_app_test(self, container_arg):
        """
        Test checks if php-version is proper one
        and specific pages returns expected message or return code.
        """
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(
            cid_file_name=cid_file_name, container_args=f"--user=100001 {container_arg}"
        )
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        assert VARS.VERSION in PodmanCLIWrapper.podman_exec_shell_command(
            cid_file_name=cid,
            cmd="php --version"
        )
        assert VARS.VERSION in PodmanCLIWrapper.podman_exec_shell_command(
            cid_file_name=cid,
            cmd="php --version",
            used_shell="/bin/sh"
        )

        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # This function tests PHP session
        assert self.s2i_app.test_response(
            url=cip, page="/session_test.php",
            expected_output="Passed"
        )
        # Assert tests if connect to http://<ip>:8080 works
        assert self.s2i_app.test_response(
            url=cip
        )
        # Assert tests if connect to https://<ip>:8443 works
        assert self.s2i_app.test_response(
            url=f"https://{cip}", port=8443
        )
        # test if configuration is writeable for php.ini
        assert PodmanCLIWrapper.podman_run_command_and_remove(
            cid_file_name=VARS.IMAGE_NAME,
            cmd="[ -w \\${PHP_SYSCONF_PATH}/php.ini ]",
            return_output=False
        ) == 0
        # test if php.d directory is writeable
        assert PodmanCLIWrapper.podman_run_command_and_remove(
            cid_file_name=VARS.IMAGE_NAME,
            cmd="[ -w \\${PHP_SYSCONF_PATH}/php.d ]",
            return_output=False
        ) == 0


class TestPHPClearEnvContainer:
    def setup_method(self):
        container_args = "" if VARS.OS == "rhel8" else "-e PHP_CLEAR_ENV=OFF"
        self.s2i_app = build_s2i_app(test_app, container_args=container_args)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_run_app_test(self):
        """
        Test checks if php-version is proper one
        and specific pages returns expected message or return code.
        """
        skip_clear_env_tests()
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user=100001")
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        assert VARS.VERSION in PodmanCLIWrapper.podman_exec_shell_command(
            cid_file_name=cid,
            cmd="php --version"
        )
        assert VARS.VERSION in PodmanCLIWrapper.podman_exec_shell_command(
            cid_file_name=cid,
            cmd="php --version",
            used_shell="/bin/sh"
        )

        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        # This function tests PHP session
        assert self.s2i_app.test_response(
            url=cip, page="/session_test.php",
            expected_output="Passed"
        )
        # Assert tests if connect to http://<ip>:8080 works
        assert self.s2i_app.test_response(
            url=cip
        )
        # Assert tests if connect to https://<ip>:8443 works
        assert self.s2i_app.test_response(
            url=f"https://{cip}", port=8443
        )
        # test if configuration is writeable for php.ini
        assert PodmanCLIWrapper.podman_run_command_and_remove(
            cid_file_name=VARS.IMAGE_NAME,
            cmd="test -w \\${PHP_SYSCONF_PATH}/php.ini",
            return_output=False
        ) == 0
        # test if php.d directory is writeable
        assert PodmanCLIWrapper.podman_run_command_and_remove(
            cid_file_name=VARS.IMAGE_NAME,
            cmd="test -w \\${PHP_SYSCONF_PATH}/php.d",
            return_output=False
        ) == 0
        if VARS.OS in ("rhel9", "rhel10"):
            # Checking if clear_env = no is set in /etc/php-fpm.d/www.conf file.
            file_content = PodmanCLIWrapper.podman_get_file_content(
                cid_file_name=cid,
                filename="/etc/php-fpm.d/www.conf"
            )
            for line in file_content.splitlines():
                if re.search("^clear_env = no", line):
                    break
            else:
                assert False, "'clear_env = no' not found in www.conf file."


class TestPHPNPMtestContainer:
    def setup_method(self):
        self.s2i_app = build_npm_app(test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_npm_works(self):
        """
        Test checks if NPM is valid and works properly
        """
        assert self.s2i_app.npm_works(image_name=VARS.IMAGE_NAME)
