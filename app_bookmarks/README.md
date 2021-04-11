# Bookmarks App
Read bookmarks.html and store it in marco27-web-mariadb

### play
cd ~/dev/repository/git/my_python/app_bookmarks
python3 main.py

##### SQL Fix
UPDATE `bookmarks` SET `folder`='Bookmarks Toolbar' WHERE `folder` = 'PROD'