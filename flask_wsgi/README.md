# Flask wsgi

### inspiring links
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04

# build
cd ~/dev/repository/git/my_python/flask_wsgi
python3 -m venv env && source ./env/bin/activate
pip install wheel
pip install uwsgi flask
deactivate

# run
### run flask
cd ~/dev/repository/git/my_python/flask_wsgi
source ./env/bin/activate
python3 app/routes.py 
http://localhost:5000/
ctrl+c
deactivate

# play
http://localhost:5000/
http://localhost:5000/home