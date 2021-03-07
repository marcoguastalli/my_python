##v2
Run a container with tiangolo/meinheld-gunicorn:python3.8 and Flask

### build
cd app_bookmarks/src/v2
docker-compose up -d

### run
docker-compose start
docker-compose stop

### access the container as root
docker container ls --all
docker exec -u root -t -i CONTANER-ID /bin/bash

## play
http://localhost/