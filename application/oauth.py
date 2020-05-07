from application import app, utils
import requests, json


class SpotifyOauth2:
    """This class is used to handles all authorization 
    requirements needed by the Spotify Web API 
    using the Authoriaztion Code Flow"""
    
    def __init__(self):
        #
        self.client_id = app.config['CLIENT_ID']
        self.client_secret = app.config['CLIENT_SECRET']
        self.redirect_uri = app.config['REDIRECT_URI']
    
    def get_authorization_header_basic(self):
        ''' Base 64 encoded string that contains the client ID and client secret key. 
        The field must have the format:
        Authorization: Basic *<base64 encoded client_id:client_secret>* '''

        encoded_secret = utils.encode_pair(self.client_id, self.client_secret)
        h = {
            'Authorization' : 'Basic {encoded_secret}'
        }
        return h

    def request_auth_url(self):
        """ request authorization url,
         returns the url and the state it is in or None """

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
            return [response.url, state]

    def request_access_token(self, access_code):
        """ request access and refresh tokens from Spotify """

        SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

        # request payload and header preparation
        payload = {
            'grant_type': 'authorization_code',
            'code': access_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        # send post request to Spotify & process response with json
        post_response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
        #response_data = json.loads(post_response.text)
        '''token_data = {
            'access_token': response_data['access_token'],
            'token_type': response_data['token_type'],
            'scope': response_data['scope'],
            'expires_in': response_data['expires_in'],
            'refresh_token': response_data['refresh_token']
        }'''
        print(post_response)
        return post_response.json()





            

            
           
            



