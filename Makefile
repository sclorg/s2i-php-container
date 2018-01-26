# Include common Makefile code.
BASE_IMAGE_NAME = php
TEST_IMAGE_NAME := $(BASE_IMAGE_NAME)-tests
TEST_TARGET := test/test_s2i.py
VERSIONS = 5.6 7.0 7.1
OPENSHIFT_NAMESPACES = 5.5

# HACK:  Ensure that 'git pull' for old clones doesn't cause confusion.
# New clones should use '--recursive'.
.PHONY: $(shell test -f common/common.mk || echo >&2 'Please do "git submodule update --init" first.')

include common/common.mk

build-test-container:
	docker build --network host --tag=$(TEST_IMAGE_NAME) -f ./test/Dockerfile.tests .

check-conu: build-test-container
	@# use it like this: `make check-conu TEST_TARGET=test/test_s2i.py::TestSuite::test_invoking_container`
	docker run --net=host -e IMAGE_NAME --rm -v /dev:/dev:ro -v /var/lib/docker:/var/lib/docker:ro --security-opt label=disable --cap-add SYS_ADMIN -ti -v /var/run/docker.sock:/var/run/docker.sock -v ${PWD}:/src -w /src $(TEST_IMAGE_NAME) pytest-3 -vv $(TEST_TARGET)
