# Cambios a realizar en esta rama php-72-wp

Vamos en un principio a instalar "wp-cli" (linea de comandos para wordpress). Para ello añadimos al "Dockerfile":

```

## instalamos wp-cli
RUN set -x && cd /tmp && \
  curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
  php wp-cli.phar --info && \
  chmod +x wp-cli.phar && \
  mv wp-cli.phar /usr/local/bin/wp && \
  wp --info 



```


## Fix problema

```
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.130.0.100. Set the 'ServerName' directive globally to suppress this message
[Mon Oct 07 03:00:57.036980 2019] [ssl:warn] [pid 1] AH01909: 10.130.0.100:8443:0 server certificate does NOT include an ID which matches the server name
[Mon Oct 07 03:00:57.106372 2019] [ssl:warn] [pid 1] AH01909: 10.130.0.100:8443:0 server certificate does NOT include an ID which matches the server name
[Mon Oct 07 03:00:57.106465 2019] [http2:warn] [pid 1] AH10034: The mpm module (prefork.c) is not supported by mod_http2. The mpm determines how things are processed in your server. HTTP/2 has more demands in this regard and the currently selected mpm will just not do. This is an advisory warning. Your server will continue to work, but the HTTP/2 protocol will be inactive.
[Mon Oct 07 03:00:57.106967 2019] [lbmethod_heartbeat:notice] [pid 1] AH02282: No slotmem from mod_heartmonitor
[Mon Oct 07 03:00:57.168237 2019] [mpm_prefork:notice] [pid 1] AH00163: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips configured -- resuming normal operations
[Mon Oct 07 03:00:57.168262 2019] [core:notice] [pid 1] AH00094: Command line: 'httpd -D FOREGROUND'
10.130.0.1 - - [07/Oct/2019:03:01:03 +0000] "GET /wp-admin/install.php HTTP/1.1" 404 218 "-" "kube-probe/1.11+"
10.130.0.1 - - [07/Oct/2019:03:01:04 +0000] "GET /wp-admin/install.php HTTP/1.1" 404 218 "-" "kube-probe/1.11+"
10.130.0.1 - - [07/Oct/2019:03:01:13 +0000] "GET /wp-admin/install.php HTTP/1.1" 404 218 "-" "kube-probe/1.11+"

```
#### El problema AH00558

Para intentar solucionar el primer problema AH00558 debemos configurar Acat "/opt/rh/httpd24/root/etc/httpd/conf/httpd.conf" con el ServerName "dominio" que en nuestro caso como se trata de openshift sería "my-wordpress-site-imagen-mysql.apps.srv.world".

Para ello en el Dockerfile vamos a crear una variable de entorno llamada "SERVERNAME" de la siguiente manara, poniendo por defecto el varlor" www.ejemplo.com":

```
SERVERNAME=${SERVERNAME:-www.ejemplo.com}
```

Recordar que al generar el contenedor debemos darle el valor apropiado a la variable "SERVERNAME".

Para que se refleje en el archivo de configuración añadimos el archivo "/home/emilio/cloud/aws/wordpress_openshift/crear_imagenes/php_base/s2i-php-container/7.2/root/usr/share/container-scripts/php/httpd-cnf/00-servername.conf" con el siguiente contenido:

```
ServerName "${SERVERNAME}"

```

Se puede poner en archivos separados con la extension ".conf" o bien en el mismo archivo "00-documentroot.conf" uno en cada línea, quedándonos "00-documentroot.conf" de la siguiente forma:



```
DocumentRoot "/opt/app-root/src${DOCUMENTROOT}"
ServerName "${SERVERNAME}"

```




#### El problema AH10034

Nos dice que apache NPM (multiprocessing module) no admite prefork. El error no parace insalvable ya que nos comenta que seguirá trabajando con http1.1.

Para solucionar este problema vamos a desactivar http2  aunque sería más interesante cambiar a otro mpm que si diera apoyo. 


Para activar:

```
$ sudo a2enmod http2

$ sudo systemctl restart apache2

```

Para desactivar: 

```
$ sudo a2dismod http2

$ sudo systemctl reload apache2

o

$ sudo service apache2 reload

o

$ sudo apachectl reset


```

Para ello vamos a intentar cambiar al mpm "event". Para ello vamos ha hacer los cambios en los archivos siguientes:

- En "s2i-php-container/7.2/root/usr/share/container-scripts/php/common.sh". 
	Comentamos la línea:
	
	# echo "LoadModule mpm_prefork_module modules/mod_mpm_prefork.so" > "${HTTPD_MODULES_CONF_D_PATH}/00-mpm.conf"
	
	Y añadimos:
	
	echo "LoadModule mpm_event_module modules/mod_mpm_event.so" > "${HTTPD_MODULES_CONF_D_PATH}/00-mpm.conf".
    
    Pero como la variable "${HTTPD_MODULES_CONF_D_PATH}" no la lee bien, especificamos el path:
    
    echo "LoadModule mpm_event_module modules/mod_mpm_event.so" > "/etc/httpd/conf.modules.d/00-mpm.conf"
    
    
    
- En "s2i-php-container/7.2/root/usr/share/container-scripts/php/httpd-cnf/50-mpm-tunning.cof", que es dónde nos configura el mpm por defecto prefork, le cambiamos la extesión del archivo y no nos cargará dicha configuración:

  s2i-php-container/7.2/root/usr/share/container-scripts/php/httpd-cnf/50-mpm-tunning_conf.old
    
Con posterioridad configuraremos event adecuadamente. Para comprobar en la imagen compilada como vemos en el apartado siguiente:

```
bash-4.2$ apachectl -V
Server version: Apache/2.4.34 (Red Hat)
Server built:   Apr 17 2019 11:29:35
Server's Module Magic Number: 20120211:79
Server loaded:  APR 1.4.8, APR-UTIL 1.5.2
Compiled using: APR 1.4.8, APR-UTIL 1.5.2
Architecture:   64-bit
Server MPM:     event
  threaded:     yes (fixed thread count)
    forked:     yes (variable process count)
Server compiled with....

```


También podemos consultar las características en http://:172.0.0.2:8080

## Vamos a compilar la imagen


```

$ cd /home/emilio/cloud/aws/wordpress_openshift/crear_imagenes/php_base/s2i-php-container


$  make build TARGET=centos7 VERSIONS=7.2


$ docker images

REPOSITORY                                                         TAG                 IMAGE ID            CREATED             SIZE
<none>                                                              <none>              7cb682102a12        54 seconds ago      648MB



$ docker tag 7cb682102a12 docker-registry-default.apps.srv.world/openshift/php-72-wp:0



$ docker images
REPOSITORY                                                          TAG                 IMAGE ID            CREATED             SIZE
docker-registry-default.apps.srv.world/openshift/php-72-wp          0                   7cb682102a12        7 minutes ago       648MB

$ oc whoami -t
vhMuYk91Jot2VnJuPwnqAL4zjSRbzPhMxy-jXnkUI3A



$ docker login -u dev https://docker-registry-default.apps.srv.world
Password: 
WARNING! Your password will be stored unencrypted in /home/emilio/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded


$ docker push docker-registry-default.apps.srv.world/openshift/php-72-wp:0



$ oc new-app php-72-wp:0~https://github.com/samyunodos/s2i-php-container/#php-72-wp --context-dir=test/test-app --name=mi-prueba --strategy=source


```

O para trabajar en  local:

```
$ s2i build git@github.com:samyunodos/s2i-php-container.git --ref=php-72-wp --context-dir=test/test-app docker-registry-default.apps.srv.world/openshift/php-72-wp:0  mi-prueba --loglevel=5


$ docker run -d  --name k00 -p 8080:8080 mi-prueba

$ docker exec -it k00 bash o

## Como root

$ docker exec -u 0 -it k00 bash

$ docker exec -u 0  --privileged -it k00 bash



bash-4.2# systemctl enable rh-php72-php-fpm.service
Created symlink /etc/systemd/system/multi-user.target.wants/rh-php72-php-fpm.service, pointing to /usr/lib/systemd/system/rh-php72-php-fpm.service.
bash-4.2# systemctl start rh-php72-php-fpm.service



systemctl list-unit-files --type=service | grep php-fpm



/etc/scl/conf/rh-php72-php-fpm.service!

rror. Self-hosted.

After much weeping and gnashing of teeth I found the culprit. I had not modified /etc/httpd/conf.d/php.conf.

Here are the full steps:

Code:

yum install centos-release-scl
yum install rh-php72 rh-php72-php rh-php72-php-fpm rh-php72-php-mysqlnd

Edit /etc/httpd/conf.d/php.conf:

Code:

# SetHandler application/x-httpd-php
# This is the default with php 5.4
#<FilesMatch \.php$>
#    SetHandler application/x-httpd-php
#</FilesMatch>

# This is the default for php7
<FilesMatch \.php$>
  SetHandler "proxy:fcgi://127.0.0.1:9000"
</FilesMatch>

Code:

systemctl enable rh-php72-php-fpm.service
systemctl start rh-php72-php-fpm.service
scl enable rh-php72 bash
systemctl restart httpd


```

oc new-build https://github.com/samyunodos/s2i-php-container --context-dir=7.2 --name=mi-prueba4 --strategy=docker 



bash-4.2$ cat /etc/httpd/conf.modules.d/00-mpm.conf 
# Select the MPM module which should be used by uncommenting exactly
# one of the following LoadModule lines:

# prefork MPM: Implements a non-threaded, pre-forking web server
# See: http://httpd.apache.org/docs/2.4/mod/prefork.html
LoadModule mpm_prefork_module modules/mod_mpm_prefork.so

# worker MPM: Multi-Processing Module implementing a hybrid
# multi-threaded multi-process web server
# See: http://httpd.apache.org/docs/2.4/mod/worker.html
#
#LoadModule mpm_worker_module modules/mod_mpm_worker.so

# event MPM: A variant of the worker MPM with the goal of consuming
# threads only for connections with active processing
# See: http://httpd.apache.org/docs/2.4/mod/event.html
#
#LoadModule mpm_event_module modules/mod_mpm_event.so


bash-4.2$ ls -la /var/opt/rh/rh-php72/lib/php        
total 20
drwxr-xr-x. 5 root root   4096 Oct 10 10:34 .
drwxr-xr-x. 6 root root   4096 Oct 10 10:34 ..
drwxrwx---. 2 root apache 4096 Nov 16  2018 opcache
drwxrwx---. 2 root apache 4096 Nov 16  2018 session
drwxrwx---. 2 root apache 4096 Nov 16  2018 wsdlcache


bash-4.2# ls -al /var/opt/rh/rh-php72/lib/php/
total 20
drwxr-xr-x. 5 root root   4096 Oct 10 10:34 .
drwxr-xr-x. 6 root root   4096 Oct 10 10:34 ..
drwxrwx---. 2 root apache 4096 Nov 16  2018 opcache
drwxrwx---. 2 root apache 4096 Nov 16  2018 session
drwxrwx---. 2 root apache 4096 Nov 16  2018 wsdlcache
bash-4.2# ls -al /var/opt/rh/rh-php72/lib/php/session/
total 8
drwxrwx---. 2 root apache 4096 Nov 16  2018 .
drwxr-xr-x. 5 root root   4096 Oct 10 10:34 ..
bash-4.2# chmod 777 /var/opt/rh/rh-php72/lib/php -R
bash-4.2# ls -al /var/opt/rh/rh-php72/lib/php/session/
total 16
drwxrwxrwx. 1 root    apache 4096 Oct 10 11:25 .
drwxrwxrwx. 1 root    root   4096 Oct 10 10:34 ..
-rw-------. 1 default root      0 Oct 10 11:25 sess_987a5d92a591a7efd6fbf8555a4c06f0
bash-4.2# ls /tmp/sessions/
bash-4.2# 



#!/bin/sh -e
#
# S2I save-artifacts script for the 'nginx-centos7' image.
# The save-artifacts script streams a tar archive to standard output.
# The archive contains the files and folders you want to re-use in the next build.
#
# For more information see the documentation:
#	https://github.com/openshift/source-to-image/blob/master/docs/builder_image.md
#
# Replace this with any logic that you need in order to save all of your built artifacts from
# your application so they can be reused in a future build to save time.
touch /tmp/artifact
cd /tmp
# the final step of the assemble script is to stream a tar of the artifacts to be saved, to stdout.
# This tar stream will be received by s2i and used as an input to the build
tar cf - artifact
