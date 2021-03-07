from flask import Flask

app_bookmarks = Flask(__name__)


@app_bookmarks.route('/error')
def error():
    return f'An error occurs!'


@app_bookmarks.route('/')
def index():
    html = "<a href='/home' target='_self'>Home</a>"
    return html


@app_bookmarks.route('/home')
def home():
    html = "<a href='/' target='_self'>Index</a>"
    return html


if __name__ == '__main__':
    app_bookmarks.run(host="0.0.0.0", debug=True, port=5000)