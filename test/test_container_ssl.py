import tempfile

from pathlib import Path

from container_ci_suite.container_lib import ContainerTestLib
from container_ci_suite.engines.container import ContainerImage
from container_ci_suite.utils import ContainerTestLibUtils

from conftest import VARS

self_signed_ssl = VARS.TEST_DIR / "self-signed-ssl"


def build_ssl_app(app_path: Path, container_args: str = "") -> ContainerTestLib:
    container_lib = ContainerTestLib(VARS.IMAGE_NAME)
    app_name = app_path.name
    s2i_app = container_lib.build_as_df(
        app_path=app_path,
        s2i_args=f"--pull-policy=never {container_args} {container_lib.build_s2i_npm_variables()}",
        src_image=VARS.IMAGE_NAME,
        dst_image=f"{VARS.IMAGE_NAME}-{app_name}"
    )
    return s2i_app


class TestPHPSslTestAppContainer:
    def setup_method(self):
        self.s2i_app = build_ssl_app(self_signed_ssl)

    def teardown_method(self):
        self.s2i_app.cleanup()

    def test_run_app_test(self):
        cid_file_name = self.s2i_app.app_name
        assert self.s2i_app.create_container(cid_file_name=cid_file_name, container_args="--user=100001")
        assert ContainerImage.wait_for_cid(cid_file_name=cid_file_name)
        cid = self.s2i_app.get_cid(cid_file_name=cid_file_name)
        assert cid
        cip = self.s2i_app.get_cip(cid_file_name=cid_file_name)
        assert cip
        assert self.s2i_app.test_response(
            url=f"https://{cip}", port=8443
        )
        server_cmd = f"openssl s_client -showcerts -servername {cip} -connect {cip}:8443 2>/dev/null"
        server_output = ContainerTestLibUtils.run_command(cmd=server_cmd)
        certificate_dir = tempfile.mkdtemp(prefix="/tmp/server_cert_dir")
        with open(Path(certificate_dir) / "output", mode="wt+") as f:
            f.write(server_output)
        server_cert = ContainerTestLibUtils.run_command(
            cmd=f"openssl x509 -inform pem -noout -text -in {Path(certificate_dir)}/output"
        )
        config_cmd = (f"openssl x509 -in "
                      f"{VARS.TEST_DIR}/{self.s2i_app.app_name}/httpd-ssl/certs/server-cert-selfsigned.pem"
                      f" -inform pem -noout -text")
        config_cert = ContainerTestLibUtils.run_command(cmd=config_cmd)
        assert server_cert == config_cert
