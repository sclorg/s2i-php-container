PHP Docker images
=================

[![Build and push images to Quay.io registry](https://github.com/sclorg/s2i-php-container/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/sclorg/s2i-php-container/actions/workflows/build-and-push.yml)

Images available on Quay are:
* CentOS 7 [php-72](https://quay.io/repository/centos7/php-72-centos7)
* CentOS 7 [php-73](https://quay.io/repository/centos7/php-73-centos7)
* CentOS 7 [php-74](https://quay.io/repository/centos7/php-74-centos7)
* CentOS Stream 9 [php-74](https://quay.io/repository/sclorg/php-74-c9s)
* Fedora [php-80](https://quay.io/repository/fedora/php-80)

This repository contains the source for building various versions of
the PHP application as a reproducible Docker image using
[source-to-image](https://github.com/openshift/source-to-image).
Users can choose between RHEL and CentOS based builder images.
The resulting image can be run using [podman](https://github.com/containers/libpod).

For more information about using these images with OpenShift, please see the
official [OpenShift Documentation](https://docs.okd.io/latest/using_images/s2i_images/php.html).

For more information about contributing, see
[the Contribution Guidelines](https://github.com/sclorg/welcome/blob/master/contribution.md).
For more information about concepts used in these container images, see the
[Landing page](https://github.com/sclorg/welcome).


Versions
--------
PHP versions currently supported are:
* [php-7.3](7.3)
* [php-7.4](7.4)
* [php-8.0](8.0)

RHEL versions currently supported are:
* RHEL7
* RHEL8
* RHEL9

CentOS versions currently supported are:
* CentOS7

CenOS Stream versions currently supported are:
* CentOS Stream 9

Installation
------------
To build a PHP image, choose either the CentOS or RHEL based image:
*  **RHEL based image**

    These images are available in the [Red Hat Container Catalog](https://catalog.redhat.com/software/containers/ubi8/php-74/5f521244e05bbcd88f128b63).
    To download it run:

    ```
    $ podman pull registry.access.redhat.com/ubi8/php-74
    ```

    To build a RHEL based PHP image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-php-container.git
    $ cd s2i-php-container
    $ make build TARGET=rhel8 VERSIONS=7.4
    ```

*  **CentOS based image**
    ```
    $ git clone --recursive https://github.com/sclorg/s2i-php-container.git
    $ cd s2i-php-container
    $ make build TARGET=centos7 VERSIONS=7.3
    ```

Alternatively, you can pull the CentOS image from Docker Hub via:

    $ podman pull centos7/php-73-centos7

Note: while the installation steps are calling `podman`, you can replace any such calls by `docker` with the same arguments.

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all the supported versions of PHP.**


Usage
-----
For information about usage of Dockerfile for PHP 7.4,
see [usage documentation](7.4/README.md).

For information about usage of Dockerfile for PHP 7.3,
see [usage documentation](7.3/README.md).

For information about usage of Dockerfile for PHP 8.0,
see [usage documentation](8.0/README.md).

Test
----
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple PHP application built on top of the s2i-php image.

Users can choose between testing a PHP test application based on a RHEL or CentOS image.

*  **RHEL based image**

    This image is not available as a trusted build in [Docker Index](https://index.docker.io).

    To test a RHEL8 based PHP-7.4 image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd s2i-php-container
    $ make test TARGET=rhel8 VERSIONS=7.4
    ```

*  **CentOS based image**

    ```
    $ cd s2i-php-container
    $ make test TARGET=centos7 VERSIONS=7.3
    ```

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all the supported versions of PHP.**


Repository organization
-----------------------
* **`<php-version>`**

    * **Dockerfile**

        CentOS based Dockerfile.

    * **Dockerfile.rhel7**

        RHEL based Dockerfile. In order to perform build or test actions on this
        Dockerfile you need to run the action on properly subscribed RHEL machine.

    * **`s2i/bin/`**

        This folder contains scripts that are run by [S2I](https://github.com/openshift/source-to-image):

        *   **assemble**

            Used to install the sources into the location where the application
            will be run and prepare the application for deployment (e.g. installing
            modules using npm, etc.)

        *   **run**

            This script is responsible for running the application, by using the
            application web server.

    * **`contrib/`**

        This folder contains a file with commonly used modules.

    * **`test/`**

        This folder contains the [S2I](https://github.com/openshift/source-to-image)
        test framework with a sample PHP app.

        * **`test-app/`**

            A simple PHP app used for testing purposes by the [S2I](https://github.com/openshift/source-to-image) test framework.

        * **run**

            Script that runs the [S2I](https://github.com/openshift/source-to-image) test framework.
