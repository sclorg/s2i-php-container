PHP 7.1 Docker image
================

This container image includes PHP 7.1 as a [S2I](https://github.com/openshift/source-to-image) base image for your PHP 7.1 applications.
Users can choose between RHEL and CentOS based builder images.
The RHEL image is available in the [Red Hat Container Catalog](https://access.redhat.com/containers/#/registry.access.redhat.com/rhscl/php-71-rhel7)
as registry.access.redhat.com/rhscl/php-71-rhel7.
The CentOS image is then available on [Docker Hub](https://hub.docker.com/r/centos/php-71-centos7/)
as centos/php-71-centos7.
The resulting image can be run using [Docker](http://docker.io).

Description
-----------

PHP 7.1 available as docker container is a base platform for
building and running various PHP 7.1 applications and frameworks.
PHP is an HTML-embedded scripting language. PHP attempts to make it easy for developers 
to write dynamically generated web pages. PHP also offers built-in database integration 
for several commercial and non-commercial database management systems, so writing 
a database-enabled webpage with PHP is fairly simple. The most common use of PHP coding 
is probably as a replacement for CGI scripts.

Usage
---------------------
To build a simple [php-test-app](https://github.com/sclorg/s2i-php-container/tree/master/7.1/test/test-app) application
using standalone [S2I](https://github.com/openshift/source-to-image) and then run the
resulting image with [Docker](http://docker.io) execute:

*  **For RHEL based image**
    ```
    $ s2i build https://github.com/sclorg/s2i-php-container.git --context-dir=7.1/test/test-app rhscl/php-71-rhel7 php-test-app
    $ docker run -p 8080:8080 php-test-app
    ```

*  **For CentOS based image**
    ```
    $ s2i build https://github.com/sclorg/s2i-php-container.git --context-dir=7.1/test/test-app centos/php-71-centos7 php-test-app
    $ docker run -p 8080:8080 php-test-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```

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
  * Default: .:/opt/app-root/src:/opt/rh/rh-php71/root/usr/share/pear
* **SESSION_PATH**
  * Location for session data files
  * Default: /tmp/sessions
* **SHORT_OPEN_TAG**
  * Determines whether or not PHP will recognize code between <? and ?> tags
  * Default: OFF
* **DOCUMENTROOT**
  * Path that defines the DocumentRoot for your application (ie. /public)
  * Default: /

The following environment variables set their equivalent property value in the opcache.ini file:
* **OPCACHE_MEMORY_CONSUMPTION**
  * The OPcache shared memory storage size in megabytes
  * Default: 128
* **OPCACHE_REVALIDATE_FREQ**
  * How often to check script timestamps for updates, in seconds. 0 will result in OPcache checking for updates on every request.
  * Default: 2

You can also override the entire directory used to load the PHP configuration by setting:
* **PHPRC**
  * Sets the path to the php.ini file
* **PHP_INI_SCAN_DIR**
  * Path to scan for additional ini configuration files

  You can use a custom composer repository mirror URL to download packages instead of the default 'packagist.org':

    * **COMPOSER_MIRROR**
      * Adds a custom composer repository mirror URL to composer configuration. Note: This only affects packages listed in composer.json.
    * **COMPOSER_INSTALLER**
      * Overrides the default URL for downloading Composer of https://getcomposer.org/installer. Useful in disconnected environments.


Source repository layout
------------------------

You do not need to change anything in your existing PHP project's repository.
However, if these files exist they will affect the behavior of the build process:

* **composer.json**

  List of dependencies to be installed with `composer`. The format is documented
  [here](https://getcomposer.org/doc/04-schema.md).


Hot deploy
---------------------

In order to immediately pick up changes made in your application source code, you need to run your built image with the `OPCACHE_REVALIDATE_FREQ=0` environment variable passed to the [Docker](http://docker.io) `-e` run flag:

```
$ docker run -e OPCACHE_REVALIDATE_FREQ=0 -p 8080:8080 php-app
```

To change your source code in running container, use Docker's [exec](http://docker.io) command:
```
docker exec -it <CONTAINER_ID> /bin/bash
```

After you [Docker exec](http://docker.io) into the running container, your current directory is set
to `/opt/app-root/src`, where the source code is located.


See also
--------
Dockerfile and other sources are available on https://github.com/sclorg/s2i-php-container.
In that repository you also can find another versions of PHP environment Dockerfiles.
Dockerfile for CentOS is called Dockerfile, Dockerfile for RHEL is called Dockerfile.rhel7.

Security Implications
---------------------

-p 8080:8080

     Opens  container  port  8080  and  maps it to the same port on the Host.
