from application import app, utils
from flask import session
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
    
    def get_authorization_header(self, token):
        ''' return authorization header format
            Authorization: Bearer {token} '''

        h = {
            'Authorization' : 'Bearer {}'.format(token)
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
            'scope': 'playlist-modify-private playlist-modify-public'
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
        return post_response.json()

    def refresh_access_token(self, refresh_token):
        '''
            this function is requests a new access_token using a refresh token
            returns token new access_token on success and None otherwise
        '''
        SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

        if refresh_token is None:
            return None
        #prepare header
        encoded_secret = utils.encode_pair(self.client_id, self.client_secret)
        header = {
            'Authorization': 'Basic {}'.format(encoded_secret),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # request body parameter
        token_data = session.get('access_token')

        #request
        post_response = requests.post(SPOTIFY_TOKEN_URL, 
        {
            'grant_type': 'refresh_token',
            'refresh_token': token_data['refresh_token']
        }, 
        headers=header)

        #error checking
        if post_response.status_code != 200:
            print("refresh_token error")
            print(post_response.json())
            return None
        
        token_data = post_response.json()
        return token_data



        
        


            

            
           
            



