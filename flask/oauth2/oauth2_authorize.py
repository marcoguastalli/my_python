from flask import Flask, redirect, request, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def home():
    if 'access_token' in session:
        return 'Welcome back!'
    else:
        return redirect(f'{REDIRECT_URI}?state=home')

@app.route('/login')
def login():
    authorization_url = f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=https://www.googleapis.com/auth/userinfo.profile'
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://oauth2.googleapis.com/token'
    payload = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)
    session['access_token'] = response.json()['access_token']
    return redirect('/')
