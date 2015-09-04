PHP for OpenShift - Docker images
========================================

This repository contains the source for building various versions of
the PHP application as a reproducible Docker image using
[source-to-image](https://github.com/openshift/source-to-image).
Users can choose between RHEL and CentOS based builder images.
The resulting image can be run using [Docker](http://docker.io).


Versions
---------------
PHP versions currently supported are:
* php-5.5
* php-5.6

RHEL versions currently supported are:
* RHEL7

CentOS versions currently supported are:
* CentOS7


Installation
---------------
To build a PHP image, choose either the CentOS or RHEL based image:
*  **RHEL based image**

    To build a RHEL based PHP-5.5 image, you need to run the build on a properly
    subscribed RHEL machine.

    ```
    $ git clone https://github.com/openshift/sti-php.git
    $ cd sti-php
    $ make build TARGET=rhel7 VERSION=5.5
    ```

*  **CentOS based image**
    ```
    $ git clone https://github.com/openshift/sti-php.git
    $ cd sti-php
    $ make build VERSION=5.5
    ```

Alternatively, you can pull the CentOS image from Docker Hub via:

    $ docker pull openshift/php-55-centos7

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all the supported versions of PHP.**


Usage
---------------------
To build a simple [php-test-app](https://github.com/openshift/sti-php/tree/master/5.5/test/test-app) application
using standalone [S2I](https://github.com/openshift/source-to-image) and then run the
resulting image with [Docker](http://docker.io) execute:

*  **For RHEL based image**
    ```
    $ s2i build https://github.com/openshift/sti-php.git --context-dir=5.5/test/test-app openshift/php-55-rhel7 php-test-app
    $ docker run -p 8080:8080 php-test-app
    ```

*  **For CentOS based image**
    ```
    $ s2i build https://github.com/openshift/sti-php.git --context-dir=5.5/test/test-app openshift/php-55-centos7 php-test-app
    $ docker run -p 8080:8080 php-test-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```


Test
---------------------
This repository also provides a [S2I](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple PHP application built on top of the sti-php image.

Users can choose between testing a PHP test application based on a RHEL or CentOS image.

*  **RHEL based image**

    This image is not available as a trusted build in [Docker Index](https://index.docker.io).

    To test a RHEL7 based PHP-5.5 image, you need to run the test on a properly
    subscribed RHEL machine.

    ```
    $ cd sti-php
    $ make test TARGET=rhel7 VERSION=5.5
    ```

*  **CentOS based image**

    ```
    $ cd sti-php
    $ make test VERSION=5.5
    ```

**Notice: By omitting the `VERSION` parameter, the build/test action will be performed
on all the supported versions of PHP. Since we currently only support version `5.5`
you can omit this parameter.**


Repository organization
------------------------
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
            will be run and prepare the application for deployment (eg. installing
            modules using npm, etc..)

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

* **`hack/`**

    Folder containing scripts which are responsible for the build and test actions performed by the `Makefile`.

Image name structure
------------------------
##### Structure: openshift/1-2-3

1. Platform name (lowercase) - php
2. Platform version(without dots) - 55
3. Base builder image - centos7/rhel7

Examples: `openshift/php-55-centos7`, `openshift/php-55-rhel7`

Environment variables
---------------------

To set these environment variables, you can place them as a key value pair into a `.sti/environment`
file inside your source code repository.

The following environment variables set their equivalent property value in the php.ini file:
* **ERROR_REPORTING**
  * Informs PHP of which errors, warnings and notices you would like it to take action for
  * Default: E_ALL & ~E_NOTICE
* **DISPLAY_ERRORS**
  * Controls whether or not and where PHP will output errors, notices and warnings
  * Default: ON
* **DISPLAY_STARTUP_ERRORS**
  * Cause display errors which occur during PHP's startup sequence to be handled separately from display errors
  * Default: OFF
* **TRACK_ERRORS**
  * Store the last error/warning message in $php_errormsg (boolean)
  * Default: OFF
* **HTML_ERRORS**
  * Link errors to documentation related to the error
  * Default: ON
* **INCLUDE_PATH**
  * Path for PHP source files
  * Default: .:/opt/app-root/src:/opt/rh/php55/root/usr/share/pear
* **SESSION_PATH**
  * Location for session data files
  * Default: /tmp/sessions

The following environment variables set their equivalent property value in the opcache.ini file:
* **OPCACHE_MEMORY_CONSUMPTION**
  * The OPcache shared memory storage size
  * Default: 16M

You can also override the entire directory used to load the PHP configuration by setting:
* **PHPRC**
  * Sets the path to the php.ini file
* **PHP_INI_SCAN_DIR**
  * Path to scan for additional ini configuration files

Apache .htaccess file
---------------------

In case the **DocumentRoot** of the application is nested within the source directory `/opt/app-root/src`,
users can provide their own **.htaccess** file.  This allows the overriding of Apache's behavior and
specifies how application requests should be handled. The **.htaccess** file needs to be located at the root
of the application source.
