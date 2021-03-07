##v3
Run a container with marco27/ubudev27:v1, Flask and uWSGI

### build
cd app_bookmarks/src/v3/
docker build -t app_bookmarks:v3 .

### run
docker run -d --rm --name app_bookmarks -p 5000:5000 app_bookmarks:v3

### access the image as root
docker run -it app_bookmarks:v3 /bin/bash

### play
http://127.0.0.1/
http://127.0.0.1/error
