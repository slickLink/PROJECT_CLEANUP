from flask import render_template, redirect, request
from application import app
from application.oauth import SpotifyOauth2

spotify_oauth = SpotifyOauth2()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/start')
def start_login():
    # Get the authorization url
    auth_url = spotify_oauth.request_auth_url()

    if auth_url is None:
        return 'Sorry Will be fixed soon!'
    else:
        return redirect(auth_url)
    return 'hello'

@app.route('/callback')
def callback():
    return request.args.get('code')