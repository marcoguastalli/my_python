##v4
Run a container with marco27/ubudev27:v1, Flask and uWSGI

### build
cd app_bookmarks/src/v4/
docker build -t app_bookmarks:v4 .

### run
docker run -d --rm --name app_bookmarks -p 80:80 app_bookmarks:v4

### access the image as root
docker run -it app_bookmarks:v4 /bin/bash

### play
http://127.0.0.1/
http://127.0.0.1/error
