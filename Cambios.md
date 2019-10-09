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
    
- En "s2i-php-container/7.2/root/usr/share/container-scripts/php/httpd-cnf/50-mpm-tunning.cof", que es dónde nos configura el mpm por defecto prefork, le cambiamos la extesión del archivo y no nos cargará dicha configuración:

  s2i-php-container/7.2/root/usr/share/container-scripts/php/httpd-cnf/50-mpm-tunning_conf.old
    

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


$ docker run -d  --name k00 mi-prueba

$ docker exec -it k00 bash o

## Como root

$ docker exec -u 0 -it k00 bash

$ docker exec -u 0  --privileged -it k00 bash


```


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
