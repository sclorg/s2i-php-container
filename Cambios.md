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

#### El problema AH10034

Nos dice que apache NPM (multiprocessing module) no admite prefork. El error no parace insalvable ya que nos comenta que seguirá trabajando con http1.1.

Para solucionar este problema vamos a desactivar http2  aunque sería más interesante cambiar a otro worker que si diera apoyo. 


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

