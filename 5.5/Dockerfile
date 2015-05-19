FROM openshift/base-centos7

# This image provides an Apache+PHP environment for running PHP
# applications.

MAINTAINER Ben Parees <bparees@redhat.com>

EXPOSE 8080

ENV PHP_VERSION=5.5 \
    PATH=$PATH:/opt/rh/php55/root/usr/bin

LABEL k8s.io/description="Platform for building and running PHP 5.5 applications" \
      k8s.io/display-name="Apache 2.4 with PHP 5.5" \
      openshift.io/expose-services="8080:http" \
      openshift.io/tags="builder,php,php55"

# Copy the STI scripts from the specific language image to /usr/local/sti
COPY ./.sti/bin/ /usr/local/sti

# Each language image can have 'contrib' a directory with extra files needed to
# run and build the applications.
COPY ./contrib/ /opt/openshift

# Install Apache httpd and PHP
RUN yum install -y \
    https://www.softwarecollections.org/en/scls/rhscl/httpd24/epel-7-x86_64/download/rhscl-httpd24-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/rhscl/php55/epel-7-x86_64/download/rhscl-php55-epel-7-x86_64.noarch.rpm \
    https://www.softwarecollections.org/en/scls/remi/php55more/epel-7-x86_64/download/remi-php55more-epel-7-x86_64.noarch.rpm && \
    yum install -y --setopt=tsflags=nodocs httpd24 php55 php55-php php55-php-mysqlnd php55-php-pgsql php55-php-bcmath php55-php-devel \
    php55-php-fpm php55-php-gd php55-php-intl php55-php-ldap php55-php-mbstring php55-php-mcript php55-php-pdo \
    php55-php-pecl-memcache php55-php-process php55-php-soap php55-php-opcache php55-php-xml \
    php55-php-pecl-imagick php55-php-pecl-xdebug && \
    yum clean all -y && \
    mkdir /tmp/sessions && \
    chown -R default:default /opt/openshift /tmp/sessions && \
    sed -i -f /opt/openshift/httpdconf.sed /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf && \
    chmod -R og+rwx /opt/rh/php55/root/etc && \
    chmod -R og+rwx /opt/rh/httpd24/root/var/run/httpd

USER 1001

# Set the default CMD to print the usage of the language image
CMD ["usage"]
