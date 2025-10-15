import os
import sys

from pathlib import Path
from collections import namedtuple
from pytest import skip

from container_ci_suite.utils import check_variables

if not check_variables():
    sys.exit(1)

Vars = namedtuple(
    "Vars", [
        "OS", "VERSION", "IMAGE_NAME", "IS_MINIMAL", "SHORT_VERSION", "TEST_DIR", "BRANCH_TO_TEST", "CHECK_MSG"
    ]
)
VERSION = os.getenv("VERSION")
BRANCH_TO_TEST = "master"
CHECK_MSG = "Welcome to your CakePHP"
# if VERSION == "7.4" or VERSION == "8.0":
#     BRANCH_TO_TEST = "4.X"
#     CHECK_MSG = "Welcome to CakePHP"
# if VERSION == "8.2" or VERSION == "8.3":
#     BRANCH_TO_TEST = "5.X"
#     CHECK_MSG = "Welcome to CakePHP"

VARS = Vars(
    OS=os.getenv("TARGET").lower(),
    VERSION=VERSION,
    IMAGE_NAME=os.getenv("IMAGE_NAME"),
    IS_MINIMAL="minimal" in VERSION,
    SHORT_VERSION=VERSION.replace(".", ""),
    TEST_DIR=Path(__file__).parent.absolute(),
    BRANCH_TO_TEST=BRANCH_TO_TEST,
    CHECK_MSG=CHECK_MSG,
)

TAGS = {
    "rhel8": "-ubi8",
    "rhel9": "-ubi9",
    "rhel10": "-ubi10",
}

MYSQL_TAGS = {
    "rhel8": "-el8",
    "rhel9": "-el9",
    "rhel10": "-el10",
}

IMAGE_TAG = f"mysql:8.0{MYSQL_TAGS.get(VARS.OS)}"

MYSQL_VERSION = f"8.0{MYSQL_TAGS.get(VARS.OS)}"


def skip_clear_env_tests():
    if VARS.OS == "rhel8" and VERSION == "8.2":
        skip(f"Skipping clear env tests for {VARS.VERSION} on {VARS.OS}.")
