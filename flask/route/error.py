from flask import Flask

app = Flask(__name__)


@app.route('/error')
def error():
    return f'An error occurs!'
