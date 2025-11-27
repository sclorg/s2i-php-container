PHP Docker images
=================

[![Build and push images to Quay.io registry](https://github.com/sclorg/s2i-php-container/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/sclorg/s2i-php-container/actions/workflows/build-and-push.yml)

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
Currently supported versions are visible in the following table, expand an entry to see its container registry address.
<!--
Table start
-->
||CentOS Stream 9|CentOS Stream 10|Fedora|RHEL 8|RHEL 9|RHEL 10|
|:--|:--:|:--:|:--:|:--:|:--:|:--:|
|7.4||||<details><summary>✓</summary>`registry.redhat.io/rhel8/php-74`</details>|||
|8.0|||||<details><summary>✓</summary>`registry.redhat.io/rhel9/php-80`</details>||
|8.2|||<details><summary>✓</summary>`quay.io/fedora/php-82`</details>|<details><summary>✓</summary>`registry.redhat.io/rhel8/php-82`</details>|<details><summary>✓</summary>`registry.redhat.io/rhel9/php-82`</details>||
|8.3|<details><summary>✓</summary>`quay.io/sclorg/php-83-c9s`</details>|<details><summary>✓</summary>`quay.io/sclorg/php-83-c10s`</details>|<details><summary>✓</summary>`quay.io/fedora/php-83`</details>||<details><summary>✓</summary>`registry.redhat.io/rhel9/php-83`</details>|<details><summary>✓</summary>`registry.redhat.io/rhel10/php-83`</details>|
<!--
Table end
-->

Installation
------------
To build a PHP image, choose either the CentOS or RHEL based image:
*  **RHEL based image**

    These images are available in the [Red Hat Container Catalog](https://catalog.redhat.com/software/containers/ubi10/php-83/677d36336490940dce770abe).
    To download it run:

    ```
    $ podman pull registry.access.redhat.com/ubi10/php-83
    ```

    To build a RHEL based PHP image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone --recursive https://github.com/sclorg/s2i-php-container.git
    $ cd s2i-php-container
    $ make build TARGET=rhel10 VERSIONS=8.3
    ```

*  **CentOS based image**
    ```
    $ git clone --recursive https://github.com/sclorg/s2i-php-container.git
    $ cd s2i-php-container
    $ make build TARGET=c10s VERSIONS=8.3
    ```

Alternatively, you can pull the CentOS Stream image from Docker Hub via:

    $ podman pull registry.access.redhat.com/ubi10/php-83

Note: while the installation steps are calling `podman`, you can replace any such calls by `docker` with the same arguments.

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all the supported versions of PHP.**


Usage
-----

For information about usage of Dockerfile for PHP 7.4,
see [usage documentation](7.4/README.md).

For information about usage of Dockerfile for PHP 8.0,
see [usage documentation](8.0/README.md).

For information about usage of Dockerfile for PHP 8.1,
see [usage documentation](8.1/README.md).

For information about usage of Dockerfile for PHP 8.2,
see [usage documentation](8.2/README.md).

For information about usage of Dockerfile for PHP 8.3,
see [usage documentation](8.3/README.md).

Test
----
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple PHP application built on top of the s2i-php image.

Users can choose between testing a PHP test application based on a RHEL or CentOS image.

*  **RHEL based image**

    This image is not available as a trusted build in [Docker Index](https://index.docker.io).

    To test a RHEL10 based PHP-8.3 image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd s2i-php-container
    $ make test TARGET=rhel10 VERSIONS=8.3
    ```

*  **CentOS Stream based image**

    ```
    $ cd s2i-php-container
    $ make test TARGET=c10s VERSIONS=8.3
    ```

**Notice: By omitting the `VERSIONS` parameter, the build/test action will be performed
on all the supported versions of PHP.**


Repository organization
-----------------------
* **`<php-version>`**

    * **Dockerfile.c10s**

        CentOS Stream based Dockerfile.

    * **Dockerfile.rhel8**

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
