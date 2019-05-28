PHP 7.0 Docker image
================

This container image includes PHP 7.0 as a [S2I](https://github.com/openshift/source-to-image) base image for your PHP 7.0 applications.
Users can choose between RHEL and CentOS based builder images.
The RHEL images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/),
the CentOS images are available on [Docker Hub](https://hub.docker.com/r/centos/),
and the Fedora images are available in [Fedora Registry](https://registry.fedoraproject.org/).
The resulting image can be run using [podman](https://github.com/containers/libpod).

Note: while the examples in this README are calling `podman`, you can replace any such calls by `docker` with the same arguments

Description
-----------

PHP 7.0 available as container is a base platform for
building and running various PHP 7.0 applications and frameworks.
PHP is an HTML-embedded scripting language. PHP attempts to make it easy for developers 
to write dynamically generated web pages. PHP also offers built-in database integration 
for several commercial and non-commercial database management systems, so writing 
a database-enabled webpage with PHP is fairly simple. The most common use of PHP coding 
is probably as a replacement for CGI scripts.

This container image includes an npm utility, so users can use it to install JavaScript
modules for their web applications. There is no guarantee for any specific npm or nodejs
version, that is included in the image; those versions can be changed anytime and
the nodejs itself is included just to make the npm work.

Usage
---------------------
For this, we will assume that you are using the `rhscl/php-70-rhel7 image`, available via `php:7.0` imagestream tag in Openshift.
Building a simple [php-test-app](https://github.com/sclorg/s2i-php-container/tree/master/7.0/test/test-app) application
in Openshift can be achieved with the following step:

    ```
    oc new-app php:7.0~https://github.com/sclorg/s2i-php-container.git --context-dir=7.0/test/test-app/
    ```

The same application can also be built using the standalone [S2I](https://github.com/openshift/source-to-image) application on systems that have it available:

    ```
    $ s2i build https://github.com/sclorg/s2i-php-container.git --context-dir=7.0/test/test-app/ rhscl/php-70-rhel7 php-sample-app
    ```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```

Environment variables
---------------------

To set these environment variables, you can place them as a key value pair into a `.s2i/environment`
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
  * Default: .:/opt/app-root/src:/opt/rh/rh-php70/root/usr/share/pear
* **PHP_MEMORY_LIMIT**
  * Memory Limit
  * Default: 128M
* **SESSION_NAME**
  * Name of the session
  * Default: PHPSESSID
* **SESSION_HANDLER**
  * Method for saving sessions
  * Default: files
* **SESSION_PATH**
  * Location for session data files
  * Default: /tmp/sessions
* **SESSION_COOKIE_DOMAIN**
  * The domain for which the cookie is valid.
  * Default: 
* **SESSION_COOKIE_HTTPONLY**
  * Whether or not to add the httpOnly flag to the cookie
  * Default: 0
* **SESSION_COOKIE_SECURE**
  * Specifies whether cookies should only be sent over secure connections.
  * Default: Off
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

You can override the Apache [MPM prefork](https://httpd.apache.org/docs/2.4/mod/mpm_common.html)
settings to increase the performance for of the PHP application. In case you set
some Cgroup limits, the image will attempt to automatically set the
optimal values. You can override this at any time by specifying the values
yourself:

* **HTTPD_START_SERVERS**
  * The [StartServers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#startservers)
    directive sets the number of child server processes created on startup.
  * Default: 8
* **HTTPD_MAX_REQUEST_WORKERS**
  * The [MaxRequestWorkers](https://httpd.apache.org/docs/2.4/mod/mpm_common.html#maxrequestworkers)
    directive sets the limit on the number of simultaneous requests that will be served.
  * `MaxRequestWorkers` was called `MaxClients` before version httpd 2.3.13.
  * Default: 256 (this is automatically tuned by setting Cgroup limits for the container using this formula:
    `TOTAL_MEMORY / 15MB`. The 15MB is average size of a single httpd process.

  You can use a custom composer repository mirror URL to download packages instead of the default 'packagist.org':

    * **COMPOSER_MIRROR**
      * Adds a custom composer repository mirror URL to composer configuration. Note: This only affects packages listed in composer.json.
    * **COMPOSER_INSTALLER**
      * Overrides the default URL for downloading Composer of https://getcomposer.org/installer. Useful in disconnected environments.
    * **COMPOSER_ARGS**
      * Adds extra arguments to the `composer install` command line (for example `--no-dev`).

Source repository layout
------------------------

You do not need to change anything in your existing PHP project's repository.
However, if these files exist they will affect the behavior of the build process:

* **composer.json**

  List of dependencies to be installed with `composer`. The format is documented
  [here](https://getcomposer.org/doc/04-schema.md).


* **.htaccess**

  In case the **DocumentRoot** of the application is nested within the source directory `/opt/app-root/src`,
  users can provide their own Apache **.htaccess** file.  This allows the overriding of Apache's behavior and
  specifies how application requests should be handled. The **.htaccess** file needs to be located at the root
  of the application source.

Hot deploy
---------------------

In order to immediately pick up changes made in your application source code, you need to run your built image with the `OPCACHE_REVALIDATE_FREQ=0` environment variable passed to [Podman](https://github.com/containers/libpod) `-e` run flag:

```
$ podman run -e OPCACHE_REVALIDATE_FREQ=0 -p 8080:8080 php-app
```

To change your source code in running container, use Podman's [exec](https://github.com/containers/libpod)) command:
```
podman exec -it <CONTAINER_ID> /bin/bash
```

After you [Podman exec](https://github.com/containers/libpod) into the running container, your current directory is set
to `/opt/app-root/src`, where the source code is located.


Extending image
---------------
Not only content, but also startup scripts and configuration of the image can
be extended using [source-to-image](https://github.com/openshift/source-to-image).

The structure of the application can look like this:

| Folder name       | Description                |
|-------------------|----------------------------|
| `./httpd-cfg`     | Can contain additional Apache configuration files (`*.conf`)|
| `./httpd-ssl`     | Can contain own SSL certificate (in `certs/` subdirectory) and key (in `private/` subdirectory)|
| `./php-pre-start`| Can contain shell scripts (`*.sh`) that are sourced before `httpd` is started|
| `./php-post-assemble`| Can contain shell scripts (`*.sh`) that are sourced at the end of `assemble` script|
| `./`              | Application source code |


See also
--------
Dockerfile and other sources are available on https://github.com/sclorg/s2i-php-container.
In that repository you also can find another versions of Python environment Dockerfiles.
Dockerfile for CentOS is called `Dockerfile`, Dockerfile for RHEL7 is called `Dockerfile.rhel7`,
for RHEL8 it's `Dockerfile.rhel8` and the Fedora Dockerfile is called Dockerfile.fedora.

Security Implications
---------------------

-p 8080:8080

     Opens  container  port  8080  and  maps it to the same port on the Host.
