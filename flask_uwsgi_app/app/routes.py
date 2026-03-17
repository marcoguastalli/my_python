from flask import Flask

app = Flask(__name__)


@app.route('/error')
def error():
    return f'An error occurs!'


@app.route('/')
def index():
    html = "<a href='/home' target='_self'>Home</a>"
    return html


@app.route('/home')
def home():
    html = "<a href='/' target='_self'>Index</a>"
    return html


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7070)