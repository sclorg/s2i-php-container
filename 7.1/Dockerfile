FROM centos/s2i-base-centos7

# This image provides an Apache+PHP environment for running PHP
# applications.

EXPOSE 8080

ENV PHP_VERSION=7.1 \
    PATH=$PATH:/opt/rh/rh-php71/root/usr/bin

ENV SUMMARY="Platform for building and running PHP $PHP_VERSION applications" \
    DESCRIPTION="PHP $PHP_VERSION available as docker container is a base platform for \
building and running various PHP $PHP_VERSION applications and frameworks. \
PHP is an HTML-embedded scripting language. PHP attempts to make it easy for developers \
to write dynamically generated web pages. PHP also offers built-in database integration \
for several commercial and non-commercial database management systems, so writing \
a database-enabled webpage with PHP is fairly simple. The most common use of PHP coding \
is probably as a replacement for CGI scripts."

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="Apache 2.4 with PHP 7.1" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,php,php71,rh-php71" \
      name="centos/php-71-centos7" \
      com.redhat.component="rh-php71-docker" \
      version="7.1" \
      release="1" \
      maintainer="SoftwareCollections.org <sclorg@redhat.com>"

# Install Apache httpd and PHP
RUN yum install -y centos-release-scl && \
    yum-config-manager --enable centos-sclo-rh-testing && \
    INSTALL_PKGS="rh-php71 rh-php71-php rh-php71-php-mysqlnd rh-php71-php-pgsql rh-php71-php-bcmath \
                  rh-php71-php-gd rh-php71-php-intl rh-php71-php-ldap rh-php71-php-mbstring rh-php71-php-pdo \
                  rh-php71-php-process rh-php71-php-soap rh-php71-php-opcache rh-php71-php-xml \
                  rh-php71-php-gmp rh-php71-php-pecl-apcu" && \
    yum install -y --setopt=tsflags=nodocs $INSTALL_PKGS --nogpgcheck && \
    rpm -V $INSTALL_PKGS && \
    yum clean all -y

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# In order to drop the root user, we have to make some directories world
# writeable as OpenShift default security model is to run the container under
# random UID.
RUN sed -i -f /opt/app-root/etc/httpdconf.sed /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf && \
    sed -i '/php_value session.save_path/d' /opt/rh/httpd24/root/etc/httpd/conf.d/rh-php71-php.conf && \
    head -n151 /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf | tail -n1 | grep "AllowOverride All" || exit && \
    echo "IncludeOptional /opt/app-root/etc/conf.d/*.conf" >> /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf && \
    mkdir /tmp/sessions && \
    chown -R 1001:0 /opt/app-root /tmp/sessions && \
    chmod -R a+rwx /tmp/sessions && \
    chmod -R ug+rwx /opt/app-root && \
    chmod -R a+rwx /etc/opt/rh/rh-php71 && \
    chmod -R a+rwx /opt/rh/httpd24/root/var/run/httpd

USER 1001

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage
