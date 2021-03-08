##v3
Run a container with tiangolo/uwsgi-nginx:python3.8, Flask and uWSGI

### build
cd app_bookmarks/src/v3/
docker build -t app_bookmarks:v3 .

### run
docker run -d --rm --name app_bookmarks -p 80:80 app_bookmarks:v3

### access the image as root
docker run -it app_bookmarks:v3 /bin/bash

### play
http://127.0.0.1/
