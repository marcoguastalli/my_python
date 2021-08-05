# flask uwsgi

### inspiring links
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04

# build
cd ~/dev/repository/gitpy/my_python/flask_uwsgi/app
python3 -m venv env && source ./env/bin/activate
pip install wheel
pip install uwsgi flask
deactivate

# run
### run flask
cd ~/dev/repository/gitpy/my_python/flask_uwsgi/app
python3 routes.py 
http://localhost:7070/
ctrl+c

### run uwsgi
cd ~/dev/repository/gitpy/my_python/flask_uwsgi/app
source ./env/bin/activate
uwsgi --socket 0.0.0.0:7070 --protocol=http -w wsgi:app
ALLOW PORT ON FIREWALL
http://localhost:7070/
ctrl+c
deactivate

# play
http://localhost:7070/
http://localhost:7070/home