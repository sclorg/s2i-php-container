Dockerfile examples
===================

This directory contains example Dockerfiles that demonstrate how to use the image with a Dockerfile and `podman build`.

For demonstration, we use an application code available at https://github.com/sclorg/cakephp-ex.git.

Pull the source to the local machine first:
```
git clone https://github.com/sclorg/cakephp-ex.git app-src
```

Then, build a new image from a Dockerfile in this directory:
```
podman build -f Dockerfile -t cakephp-app .
```

And run the resulting image with the final application:
```
podman run -ti --rm cakephp-app
```

