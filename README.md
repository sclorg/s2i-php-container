PHP for OpenShift - Docker images
========================================

This repository contains sources of the images for building various versions
of PHP applications as reproducible Docker images using
[source-to-image](https://github.com/openshift/source-to-image).
User can choose between RHEL and CentOS based builder images.
The resulting image can be run using [Docker](http://docker.io).


Versions
---------------
PHP versions currently supported are:
* php-5.5

RHEL versions currently supported are:
* RHEL7

CentOS versions currently supported are:
* CentOS7


Installation
---------------
To build a PHP image, choose between a CentOS or RHEL based image:
*  **RHEL based image**

    To build a rhel-based php-5.5 image, you need to run the build on a properly
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
on all the supported versions of PHP. Since we are currently only support version `5.5`,
you can omit this parameter.**


Usage
---------------------
To build simple [php-test-app](https://github.com/openshift/sti-php/tree/master/5.5/test/test-app) application,
using standalone [STI](https://github.com/openshift/source-to-image) and then run the
resulting image with [Docker](http://docker.io) execute:

*  **For RHEL based image**
    ```
    $ sti build https://github.com/openshift/sti-php.git --contextDir=5.5/test/test-app openshift/php-55-rhel7 php-test-app
    $ docker run -p 8080:8080 php-test-app
    ```

*  **For CentOS based image**
    ```
    $ sti build https://github.com/openshift/sti-php.git --contextDir=5.5/test/test-app openshift/php-55-centos7 php-test-app
    $ docker run -p 8080:8080 php-test-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```


Test
---------------------
This repository also provides [STI](https://github.com/openshift/source-to-image) test framework,
which launches tests to check functionality of a simple php application built on top of sti-php image.

User can choose between testing php test application based on RHEL or CentOS image.

*  **RHEL based image**

    This image is not available as trusted build in [Docker Index](https://index.docker.io).

    To test a rhel7-based php-5.5 image, you need to run the test on a properly
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

    * **`.sti/bin/`**

        This folder contains scripts that are run by [STI](https://github.com/openshift/source-to-image):

        *   **assemble**

            Is used to install the sources into location from where the application
            will be run and prepare the application for deployment (eg. installing
            modules using npm, etc..)

        *   **run**

            This script is responsible for running the application, by using the
            application web server.

    * **`contrib/`**

        This folder contains file with commonly used modules.

    * **`test/`**

        This folder contains a simple [STI](https://github.com/openshift/source-to-image)
        test framework with a sample PHP app.

        * **`test-app/`**

            Simple PHP app for used for testing purposes in the [STI](https://github.com/openshift/source-to-image) test framework.

        * **run**

            Script that runs the [STI](https://github.com/openshift/source-to-image) test framework.

* **`hack/`**

    Folder contains scripts which are responsible for build and test actions performed by the `Makefile`.

Image name structure
------------------------
##### Structure: openshift/1-2-3

1. Platform name - php
2. Platform version(without dots)
3. Base builder image - centos7/rhel7

Examples: `openshift/php-55-centos7`, `openshift/php-55-rhel7`

Environment variables
---------------------

To set these environment variables, you can place them into `.sti/environment`
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
  * Default: .:/opt/openshift/src:/opt/rh/php55/root/usr/share/pear
* **SESSION_PATH**
  * Location for session data files
  * Default: /tmp/sessions

The following environment variables set their equivalent property value in the opcache.ini file:
* **OPCACHE_MEMORY_CONSUMPTION**
  * The OPcache shared memory storage size
  * Default: 16M

dummy change3
