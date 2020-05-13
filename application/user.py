import requests
from application import utils

class User:
    '''
        This Class is used to store data related to the user
        Including information from spotify '''
    
    def __init__(self):
        ''' playlist format (dict):
        id : <id>,
        image : <image_url>,
        name : <name>,
        tracks: <tracks_url>
        '''
        self.playlists = []
        self.user_id = None
    
    def delete_tracks(self, auth_header ,playlist_id, track_ids):
        '''
            given a list of valid track ids,
            will request spotify to delete the tracks from a playlist
        '''
        SPOTIFY_USER_PLAYLIST = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
        if auth_header is None:
            return False
        else:
            auth_header['Content-Type'] = 'application/json'
        # data format
        data_payload = {
            'tracks': None
        }
        data = []
        for track in track_ids:
            template = {
                'uri': 'spotify:track:{}'.format(track)
            }
            data.append(template)
        data_payload['tracks'] = data


        
        

        


    def process_tracks(self, data):
        '''
            takes unprocessed Spotify track objects 
            returns a <list> of processed tracks or None
        '''
        tracks = []

        for item in data:
            track_template = {
                'id': None,
                'image': None,
                'name': None,
                'artists': None,
                'duration': None
            }
            # retrieve id
            track_template['id'] = item['track']['id']
            # retrieve album image
            track_template['image'] = item['track']['album']['images'][0]['url']
            # retrieve track name
            track_template['name'] = item['track']['name']
            # retrieve artist names
            artists_list = item['track']['artists']
            artists = ''
            for artist in artists_list:
                artists += artist['name'] + ', '
            
            track_template['artists'] = artists[:-2]
            # retrieve track duration
            track_template['duration'] = utils.convert_time(item['track']['duration_ms'])
            tracks.append(track_template)
        
        return tracks


    
    def request_playlist_tracks(self, auth_header, playlist_id):
        '''
            Requests tracks from a given playlist_id
            returns: list of tracks with template:
            track format <dict>
            id: <id>,
            image: <album_image_url>,
            name: <name>,
            artist: <artist>
            duration: <time>
        '''
        SPOTIFY_USER_PLAYLIST = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
        tracks = []

        if (auth_header is None):
            return None
        
        # get data
        get_response = requests.get(SPOTIFY_USER_PLAYLIST, headers=auth_header)

        #error checking
        if (get_response.status_code != 200):
            print(get_response.json())
            return None
        
        #process response
        response_data = get_response.json()
        tracks_data = response_data['items']
        tracks.extend(self.process_tracks(tracks_data))

        # check for paging object - more playlist data
        while(response_data['next'] is not None):
            #get data
            next_set = requests.get(response_data['next'], headers=auth_header)
            #error checking
            if (next_set.status_code != 200):
                print(next_set.json())
                break

            #process more data
            response_data = next_set.json()
            tracks_data = response_data['items']
            tracks.extend(self.process_tracks(tracks_data))

        return tracks



    
    def process_playlists(self, playlists_data):
        ''' 
            This function strips useful playlist info given by spotify
            takes an array of playlist objects from spotify
            formats each playlist owned by the user to python <dict>
            then adds formated playlist item to self.playlists
        '''
        for item in playlists_data:
            playlist_template = {
                'id': None,
                'image': None,
                'name': None,
                'tracks': None
            }
            #check is playlist is owned by user
            if (item['owner']['display_name'] == self.user_id):
                playlist_template['id'] = item['id']
                # playlist could have no image b/c there are no tracks
                try:
                    playlist_template['image'] = item['images'][0]['url']
                except IndexError:
                    playlist_template['image'] = None
                playlist_template['name'] = item['name']
                # playlist could have no tracks
                try:
                    playlist_template['tracks'] = item['tracks']['href']
                except:
                    playlist_template['tracks'] = None
                #add processed playlist to user playlists
                self.playlists.append(playlist_template)
        return

    def request_user_playlists(self, auth_header):
        '''
            request user playlists from Spotify 
            return: True on success, False on failure
        '''
        self.playlists.clear()
        SPOTIFY_USER_PLAYLISTS = 'https://api.spotify.com/v1/me/playlists'

        if (auth_header is None):
            return False
        # get data
        get_response = requests.get(SPOTIFY_USER_PLAYLISTS, headers=auth_header, params={'limit': 50})
        #error checking
        if(get_response.status_code != 200):
            print(get_response.json())
            return False
        #process data
        response_data = get_response.json()
        playlist_data = response_data['items']
        self.process_playlists(playlist_data)
        
        # check for paging object - more playlist data
        while(response_data['next'] is not None):
            #get data
            next_set = requests.get(response_data['next'], headers=auth_header, params={'limit': 20})
            #error checking
            if (next_set.status_code != 200):
                print(next_set.json())
                break

            #process more data
            response_data = next_set.json()
            playlist_data = response_data['items']
            self.process_playlists(playlist_data)
        return True






    def request_user_data(self, auth_header):
        ''' 
            request user info from Spotify and fill to this class
            returns: True on success, False otherwise
            
            sadly: this function is not needed :( read API 
            and plan next time. '''

        SPOTIFY_USER_PROFILE_URL = 'https://api.spotify.com/v1/me'

        if (auth_header is None):
            return False
        # get data
        get_response = requests.get(SPOTIFY_USER_PROFILE_URL, headers=auth_header)
        
        #error checking
        if(get_response.status_code != 200):
            print(get_response.json())
            return False
        
        user_data = get_response.json()
        self.user_id = user_data['id']
        return True 

        
