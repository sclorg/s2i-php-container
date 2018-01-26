#!/usr/bin/python3
import logging
import os
import time

from conu import DockerBackend, S2IDockerImage, Probe, DockerRunBuilder

import pytest


image_name = os.environ.get("IMAGE_NAME", "php")
test_dir = os.path.abspath(os.path.dirname(__file__))
test_app_path = os.path.join(test_dir, "test-app")
app_paths = [
    test_app_path
]


backend = DockerBackend(logging_level=logging.DEBUG)


@pytest.fixture(scope="module", params=app_paths)
def app(request):
    i = S2IDockerImage(image_name)
    app_name = os.path.basename(request.param)
    app = i.extend(request.param, app_name)
    yield app
    pass
    app.rmi()


class GenericTestSuite:
    def _generic_test_s2i_apps(self, app, check_cmd, expected_output, port=8080):
        c = app.run_via_binary()
        try:
            c.wait_for_port(port)
            assert c.is_port_open(port)
            response = c.http_request("/", port=port)
            assert response.ok
            output = c.execute(check_cmd)
            assert expected_output in output.decode("utf-8")
        finally:
            c.stop()
            c.wait()
            # debugging
            print(c.logs())
            c.delete()

    def _generic_test_invoking_container(self, check_cmd, expected_output):
        image = backend.ImageClass(image_name)
        c = image.run_via_binary(DockerRunBuilder(command=check_cmd))
        try:
            c.wait()
            assert expected_output in c.logs().decode("utf-8")
        finally:
            c.stop()
            c.wait()
            c.delete()

    def _generic_test_usage(self):
        i = S2IDockerImage(image_name)
        c = i.run_via_binary()

        def logs_received():
            return len(c.logs()) > 0

        try:
            c.wait()
            # even after waiting there is still a race in journal logging driver
            Probe(timeout=10, pause=0.05, count=20, fnc=logs_received).run()
            logs = c.logs().decode("utf-8").strip()
            usage = i.usage()
            # FIXME: workaround: `docker logs` can't handle logs like these: '\n\n\n'
            assert logs.replace("\n", "") == usage.replace("\n", "")
        finally:
            c.delete()

class TestSuite(GenericTestSuite):
    def test_s2i_apps(self, app):
        self._generic_test_s2i_apps(app, ["php", "--version"], "PHP 7.1.")
    def test_invoking_container(self):
        self._generic_test_invoking_container(["php", "--version"], "PHP 7.1.")
    def test_usage(self):
        self._generic_test_usage()


