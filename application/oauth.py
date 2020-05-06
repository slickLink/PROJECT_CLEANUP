from application import app, utils
import requests


class SpotifyOauth2:
    """This class is used to handles all authorization 
    requirements needed by the Spotify Web API 
    using the Authoriaztion Code Flow"""
    
    def __init__(self):
        #
        self.client_id = app.config['CLIENT_ID']
        self.client_secret = app.config['CLIENT_SECRET']
        self.redirect_uri = app.config['REDIRECT_URI']

    def request_auth_url(self):
        """ request authorization url,
         returns the url or None """

        SPOTIFY_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'

        # protect against attacks such as cross-site request forgery using state
        state = utils.random_string(10)
        parameters = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'state': state,
            'scope': 'playlist-modify-private'
        }

        # request authorization code
        response = requests.get(SPOTIFY_AUTHORIZE_URL, params=parameters)
            
        if response.status_code != 200:
            return None
        else:
            return response.url
        

            

            
           
            



