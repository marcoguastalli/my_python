# flask uwsgi app (v2)

# build
cd ~/dev/repository/git/my_python/flask_uwsgi_app/app
python3 -m venv env && source ./env/bin/activate
pip install wheel
pip install uwsgi flask
deactivate

# run
### run flask
cd ~/dev/repository/git/my_python/flask_uwsgi_app/app
python3 routes.py 
http://localhost:7070/
ctrl+c

### run uwsgi
cd ~/dev/repository/git/my_python/flask_uwsgi_app/app
source ./env/bin/activate
uwsgi --socket 0.0.0.0:7070 --protocol=http -w wsgi:app
ALLOW PORT ON FIREWALL
http://localhost:7070/
ctrl+c
deactivate

# play
http://localhost:7070/
http://localhost:7070/home