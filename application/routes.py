from flask import render_template, redirect, request, url_for, make_response, session
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
    auth_url_state = spotify_oauth.request_auth_url()
    if auth_url_state is None:
        return 'Sorry Will be fixed soon!'
    else:
        #save state in session
        session['state'] = auth_url_state[1]
    return redirect(auth_url_state[0])

@app.route('/callback')
def callback():
    #check if user did not grant access 
    error_check = request.args.get('error') or None
    if error_check is None:
        # send user back to welcome page
        return redirect(url_for('start_login'))
    
    # check for cross-site request forgery
    check_state = session.get('state')
    returned_state = request.args.get('state')
    if check_state == returned_state:
        return 'True'
    else:
        return 'False'