import os
import sys

from pathlib import Path
from collections import namedtuple
from pytest import skip

from container_ci_suite.utils import check_variables

if not check_variables():
    sys.exit(1)

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10",
}

Vars = namedtuple(
    "Vars", [
        "OS", "TAG", "VERSION", "IMAGE_NAME", "IS_MINIMAL",
        "SHORT_VERSION", "TEST_DIR", "BRANCH_TO_TEST", "CHECK_MSG"
    ]
)
VERSION = os.getenv("VERSION")
OS = os.getenv("TARGET").lower()

VARS = Vars(
    OS=OS,
    TAG=TAGS.get(OS),
    VERSION=VERSION,
    IMAGE_NAME=os.getenv("IMAGE_NAME"),
    IS_MINIMAL="minimal" in VERSION,
    SHORT_VERSION=VERSION.replace(".", ""),
    TEST_DIR=Path(__file__).parent.absolute(),
    BRANCH_TO_TEST="master",
    CHECK_MSG="Welcome to your CakePHP",
)


def skip_clear_env_tests():
    if VARS.OS == "rhel8" and VERSION == "8.2":
        skip(f"Skipping clear env tests for {VARS.VERSION} on {VARS.OS}.")
