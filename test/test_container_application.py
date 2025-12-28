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


class TestHTTPDRemoteIPContainer:
    def setup_method(self):
        container_args = "-e HTTPD_ENABLE_REMOTEIP=1"
        self.s2i_app = build_s2i_app(test_app, container_args=container_args)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_remoteip_config_created(self):
        """
        Test checks if remoteip.conf is created when HTTPD_ENABLE_REMOTEIP=1
        and contains the expected Apache mod_remoteip configuration.
        """
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user=100001")
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid

        # Wait for container to fully start and run pre-start scripts
        import time
        time.sleep(5)

        # Verify remoteip.conf exists and contains expected directives
        file_content = PodmanCLIWrapper.podman_get_file_content(
            cid_file_name=cid,
            filename="/opt/app-root/etc/conf.d/remoteip.conf"
        )
        assert file_content, "remoteip.conf file should exist"

        # Check for required mod_remoteip directives
        required_directives = [
            "LoadModule remoteip_module modules/mod_remoteip.so",
            "RemoteIPHeader X-Forwarded-For",
            "RemoteIPTrustedProxy 10.0.0.0/8",
            "RemoteIPTrustedProxy 172.16.0.0/12",
            "RemoteIPTrustedProxy 192.168.0.0/16",
            "RemoteIPTrustedProxy 169.254.0.0/16",
            "RemoteIPTrustedProxy 127.0.0.0/8",
        ]

        for directive in required_directives:
            assert directive in file_content, f"Missing directive: {directive}"

    def test_remoteip_container_runs(self):
        """
        Test checks if container with HTTPD_ENABLE_REMOTEIP=1 starts successfully
        and serves content properly.
        """
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user=100001")
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid

        # Wait for container to fully start
        import time
        time.sleep(5)

        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)

        # Only test HTTP responses if container has an IP (may not work in some rootless environments)
        if cip:
            # Verify container is serving content properly
            assert self.s2i_app.test_response(url=cip)

            # Verify HTTPS also works
            assert self.s2i_app.test_response(
                url=f"https://{cip}", port=8443
            )


class TestHTTPDRemoteIPDisabledContainer:
    def setup_method(self):
        # Build without HTTPD_ENABLE_REMOTEIP environment variable
        self.s2i_app = build_s2i_app(test_app)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_remoteip_disabled_by_default(self):
        """
        Test checks if mod_remoteip is NOT enabled by default
        when HTTPD_ENABLE_REMOTEIP is not set.
        """
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user=100001")
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid

        # Wait for container to fully start
        import time
        time.sleep(5)

        # Verify remoteip.conf does NOT exist
        result = PodmanCLIWrapper.podman_exec_shell_command(
            cid_file_name=cid,
            cmd="test -f /opt/app-root/etc/conf.d/remoteip.conf && echo exists || echo missing"
        )
        assert "missing" in result, "remoteip.conf should not exist when HTTPD_ENABLE_REMOTEIP is not set"

        # Verify container still runs properly without remoteip
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)

        # Only test HTTP response if container has an IP (may not work in some rootless environments)
        if cip:
            assert self.s2i_app.test_response(url=cip)
