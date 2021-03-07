##v1
Run a container with tiangolo/meinheld-gunicorn:python3.8 and Flask

### build
cd app_bookmarks/src/v1
docker build -t app_bookmarks:v1 .

### run
docker run -d --rm --name app_bookmarks -p 80:80 app_bookmarks:v1

### access the image as root
docker run -it app_bookmarks:v1 /bin/bash

#play
http://localhost/