FROM openshift/base-centos7

# This image provides an Apache+PHP environment for running PHP
# applications.

MAINTAINER SoftwareCollections.org <sclorg@redhat.com>

EXPOSE 8080

ENV PHP_VERSION=5.5 \
    PATH=$PATH:/opt/rh/php55/root/usr/bin

LABEL io.k8s.description="Platform for building and running PHP 5.5 applications" \
      io.k8s.display-name="Apache 2.4 with PHP 5.5" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,php,php55"

# Install Apache httpd and PHP
RUN yum install -y centos-release-scl && \
    INSTALL_PKGS="httpd24 php55 php55-php php55-php-mysqlnd php55-php-pgsql php55-php-bcmath php55-php-devel \
                  php55-php-fpm php55-php-gd php55-php-intl php55-php-ldap php55-php-mbstring php55-php-pdo \
                  php55-php-pecl-memcache php55-php-process php55-php-soap php55-php-opcache php55-php-xml \
                  php55-php-gmp" && \
    yum install -y --setopt=tsflags=nodocs --enablerepo=centosplus $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum -y clean all --enablerepo='*'

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Copy extra files to the image.
COPY ./root/ /

# In order to drop the root user, we have to make some directories world
# writeable as OpenShift default security model is to run the container under
# random UID.
RUN sed -i -f /opt/app-root/etc/httpdconf.sed /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf && \
    sed -i '/php_value session.save_path/d' /opt/rh/httpd24/root/etc/httpd/conf.d/php55-php.conf && \
    echo "IncludeOptional /opt/app-root/etc/conf.d/*.conf" >> /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf && \
    head -n151 /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf | tail -n1 | grep "AllowOverride All" || exit && \
    mkdir /tmp/sessions && \
    chown -R 1001:0 /opt/app-root /tmp/sessions && \
    chmod -R a+rwx /tmp/sessions && \
    chmod -R ug+rwx /opt/app-root && \
    chmod -R a+rwx /opt/rh/php55/root/etc && \
    chmod -R a+rwx /opt/rh/httpd24/root/var/run/httpd

USER 1001

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage
