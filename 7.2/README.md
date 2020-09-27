PHP 7.2 container image
================

This container image includes PHP 7.2 as a [S2I](https://github.com/openshift/source-to-image) base image for your PHP 7.2 applications.
Users can choose between RHEL and CentOS based builder images.
The RHEL UBI images are available in the [Red Hat Container Catalog](https://access.redhat.com/containers/),
and the Fedora images are available in [Fedora Registry](https://registry.fedoraproject.org/).
The resulting image can be run using [podman](https://github.com/containers/libpod).

Note: while the examples in this README are calling `podman`, you can replace any such calls by `docker` with the same arguments

Description
-----------

PHP 7.2 available as container is a base platform for
building and running various PHP 7.2 applications and frameworks.
PHP is an HTML-embedded scripting language. PHP attempts to make it easy for developers 
to write dynamically generated web pages. PHP also offers built-in database integration 
for several commercial and non-commercial database management systems, so writing 
a database-enabled webpage with PHP is fairly simple. The most common use of PHP coding 
is probably as a replacement for CGI scripts.

This container image includes an npm utility, so users can use it to install JavaScript
modules for their web applications. There is no guarantee for any specific npm or nodejs
version, that is included in the image; those versions can be changed anytime and
the nodejs itself is included just to make the npm work.

Usage in OpenShift
---------------------
In this example, we will assume that you are using the `ubi8/php-72` image, available via `php:72` imagestream tag in Openshift.

To build a simple [cakephp-sample-app](https://github.com/sclorg/cakephp-ex.git) application in Openshift:

```
oc new-app php:7.2~https://github.com/sclorg/cakephp-ex.git
```

To access the application:
```
$ oc get pods
$ oc exec <pod> -- curl 127.0.0.1:8080
```

**Accessing the application:**
```
$ curl 127.0.0.1:8080
```

Source-to-Image framework and scripts
---------------------
This image supports the [Source-to-Image](https://docs.openshift.com/container-platform/3.11/creating_images/s2i.html)
(S2I) strategy in OpenShift. The Source-to-Image is an OpenShift framework
which makes it easy to write images that take application source code as
an input, use a builder image like this PHP container image, and produce
a new image that runs the assembled application as an output.

To support the Source-to-Image framework, important scripts are included in the builder image:

* The `/usr/libexec/s2i/assemble` script inside the image is run to produce a new image with the application artifacts. The script takes sources of a given application and places them into appropriate directories inside the image. It utilizes some common patterns in PHP application development (see the **Environment variables** section below).
* The `/usr/libexec/s2i/run` script is set as the default command in the resulting container image (the new image with the application artifacts). It runs `httpd` with PHP support enabled.

Building an application using a Dockerfile
---------------------
Compared to the Source-to-Image strategy, using a Dockerfile is a more
flexible way to build a PHP container image with an application.
Use a Dockerfile when Source-to-Image is not sufficiently flexible for you or
when you build the image outside of the OpenShift environment.

To use the PHP image in a Dockerfile, follow these steps:

#### 1. Pull a base builder image to build on

```
podman pull ubi8/php-72
```

An UBI image `ubi8/php-72` is used in this example. This image is usable and freely redistributable under the terms of the UBI End User License Agreement (EULA). See more about UBI at [UBI FAQ](https://developers.redhat.com/articles/ubi-faq).

#### 2. Pull an application code

An example application available at https://github.com/sclorg/cakephp-ex.git is used here. Feel free to clone the repository for further experiments.

```
git clone https://github.com/sclorg/cakephp-ex.git app-src
```

#### 3. Prepare an application inside a container

This step usually consists of at least these parts:

* putting the application source into the container
* installing the dependencies
* setting the default command in the resulting image

For all these three parts, users can either setup all manually and use commands `./composer.phar` or other commands explicitly in the Dockerfile ([3.1.](#31-to-use-your-own-setup-create-a-dockerfile-with-this-content)), or users can use the Source-to-Image scripts inside the image ([3.2.](#32-to-use-the-source-to-image-scripts-and-build-an-image-using-a-dockerfile-create-a-dockerfile-with-this-content); see more about these scripts in the section "Source-to-Image framework and scripts" above), that already know how to set-up and run some common PHP applications.

##### 3.1. To use your own setup, create a Dockerfile with this content:
```
FROM ubi8/php-72

# Add application sources
ADD app-src .

# Install the dependencies
RUN TEMPFILE=$(mktemp) && \
    curl -o "$TEMPFILE" "https://getcomposer.org/installer" && \
    php <"$TEMPFILE" && \
    ./composer.phar install --no-interaction --no-ansi --optimize-autoloader

# Run script uses standard ways to configure the PHP application
# and execs httpd -D FOREGROUND at the end
# See more in <version>/s2i/bin/run in this repository.
# Shortly what the run script does: The httpd daemon and php needs to be
# configured, so this script prepares the configuration based on the container
# parameters (e.g. available memory) and puts the configuration files into
# the approriate places.
# This can obviously be done differently, and in that case, the final CMD
# should be set to "CMD httpd -D FOREGROUND" instead.
CMD /usr/libexec/s2i/run

```

##### 3.2. To use the Source-to-Image scripts and build an image using a Dockerfile, create a Dockerfile with this content:
```
FROM ubi8/php-72

# Add application sources to a directory that the assemble script expects them
# and set permissions so that the container runs without root access
USER 0
ADD app-src /tmp/src
RUN chown -R 1001:0 /tmp/src
USER 1001

# Install the dependencies
RUN /usr/libexec/s2i/assemble

# Set the default command for the resulting image
CMD /usr/libexec/s2i/run
```

#### 4. Build a new image from a Dockerfile prepared in the previous step

```
podman build -t cakephp-app .
```

#### 5. Run the resulting image with the final application

```
podman run -d cakephp-app
```

Environment variables for Source-to-Image
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
  * Default: .:/opt/app-root/src:/opt/rh/rh-php72/root/usr/share/pear (EL7)
  * Default: .:/opt/app-root/src:/usr/share/pear (EL8, Fedora)
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
* **OPCACHE_MAX_FILES**
  * The maximum number of keys (scripts) in the OPcache hash table. Only numbers between 200 and 1000000 are allowed.
  * Default: 4000  

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
