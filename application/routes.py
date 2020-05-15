from flask import render_template, redirect, request, url_for, make_response, session, flash
from application import app
from application.oauth import SpotifyOauth2
from application.user import User

spotify_oauth = SpotifyOauth2()
spotify_user = User()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/home')
def home():
    # send selected playlist names back to server
    return render_template("home.html", playlists=spotify_user.playlists)

@app.route('/dash', methods=['GET','POST','DELETE'])
def dash():
    if request.method == 'POST':
        # get retrive mode
        request_data = request.get_json()
        mode = request_data.get('mode')
        
        if (mode == 'get-tracks'):
            # retrieve playlist ids
            main_playlist_id = request_data.get('main')
            other_playlist_id = request_data.get('other')

            session['main'] = main_playlist_id
            session['other'] = other_playlist_id

            # retrieve access_token
            token_data = session.get('access_token')
            h = spotify_oauth.get_authorization_header(token_data['access_token'])
            # get data
            data = spotify_user.request_playlist_tracks(h, main_playlist_id)

            if data is None:
                return 'Sorry playlist has no tracks'
            session['tracks'] = data
            return url_for('dash')
        elif (mode == 'delete-tracks'):
            # retrieve tracks
            tracks = request_data.get('tracks')

            # retrieve access_token
            token_data = session.get('access_token')
            h = spotify_oauth.get_authorization_header(token_data['access_token'])
            # retrieve playlist id
            playlist_id = session.get('main')
            # delete tracks
            data = spotify_user.delete_tracks(h, playlist_id, tracks)
            tracks_data = session.get('tracks')
            if data is True:
                for item in tracks:
                    # for every deleted track id
                    for i in range(len(tracks_data)):
                        # search saved tracks and delete the version here
                        if tracks_data[i]['id'] == item:
                            del tracks_data[i]
                            break
                session['tracks'] = tracks_data
            print(data)
            return str(data)
    return render_template("dash.html", tracks=session.get('tracks'), main=session.get('main'), other=session.get('other'))

@app.route('/start')
def start_login():
    # Get the authorization url
    auth_url_state = spotify_oauth.request_auth_url()
    if auth_url_state is None:
        return 'Sorry Will be fixed soon!'

    # save state in session
    session['state'] = auth_url_state[1]
    return redirect(auth_url_state[0])


@app.route('/callback')
def callback():
    #check if user did not grant access 
    error_check = request.args.get('error') or None
    if error_check:
        # send user back to welcome page
        return redirect(url_for('index'))
    
    # check for cross-site request forgery
    check_state = session.get('state')
    returned_state = request.args.get('state')
    if check_state != returned_state:
        # tell user of error
        flash("incorrect state recieved from API request")
        redirect(url_for('index'))
    
    #get access_token and refresh token
    auth_code = request.args.get('code')
    token_data = spotify_oauth.request_access_token(auth_code)

    #save token in session
    session['access_token'] = token_data

    # get user data
    h = spotify_oauth.get_authorization_header(token_data['access_token'])
    check_request = spotify_user.request_user_data(h)
    if (not check_request):
        flash("error: unsuccessful user data retrieval")
    
    # get user's playlists
    check_request = spotify_user.request_user_playlists(h)
    if (not check_request):
        flash("error: unsuccessful playlist data retrieval")
    
    # user might not have any playlists (idkw don't ask)
    if (spotify_user.playlists.count == 0):
        flash("Please add playlists to your Spotify account.")
        redirect(url_for('index'))
    
    # redirect to home page so access_token is not leaked via url
    return redirect(url_for('home'))

       