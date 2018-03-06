# README
This docker image run a HatStall service on port 8000 that can be configured through environment variables

## ENVIRONMENT
### HATSTALL_GUNICORN_WORKERS
Set gunicorn number of workers (Default: 2)

### HATSTALL_GUNICORN_TIMEOUT
Set gunicorn timeout value (Default: 90)

### HATSTALL_ADMIN_USER
Set hatstall admin login (Default: admin)

### HATSTALL_ADMIN_MAIL
Set hatstall admin email address (Default: admin@example.com)

### HATSTALL_ADMIN_PASS
Set hatstall admin password (Default: admin)

### HATSTALL_DEBUG
Set debug mode (True/False)

### HATSTALL_ALLOWED_HOST
Define a list of allow host seperated by comma "host1,host2"

### SHDB_USER
Set sortinghat database username (Default: '')

### SHDB_PASS
Set sortinghat database password (Default: '')

### SHDB_NAME
Set sortinghat database name (Default: '')

### SHDB_HOST
Set sortinghat database hostname (Default: '')

### EXAMPLE
```
docker run -i -t --rm -e 'HATSTALL_ALLOWED_HOST=localhost,127.0.0.1' grimoirelab/hatstall:0.1.0
```

## DOCKER
### BUILD
In order to build new docker images, just run `make build` to create those images
with tags based on the version defined in file `../../_version.py`.

### PUBLISH
In order to publish docker images on the registry, just run `make publish` to push
docker images.
The variable 'IMAGE', in the Makefile, defines where the image will be publish.
