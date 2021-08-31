import datetime
import base64
import requests
from  urllib.parse import urlencode

class SpotifyApi(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    code_for_token = None
    client_secret = None
    auth_url = 'https://accounts.spotify.com/authorize?'
    token_url = 'https://accounts.spotify.com/api/token'
    scopes = None
    redirect_uri = None


    def __init__(self, client_id, client_secret, redirect_uri, scopes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes

    def get_auth_data(self):
        return {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri' : self.redirect_uri,
            'scope': self.scopes,
            'show_dialog': 'true'
        }

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        if self.client_id == None or self.client_secret == None:
            raise Exception('You must set client id and client secret')
        client_credentials = f'{self.client_id}:{self.client_secret}'
        return base64.b64encode(client_credentials.encode()).decode()

    def get_token_headers(self):
        client_credentials_64 = self.get_client_credentials()
        return {
            'Authorization' : f'Basic {client_credentials_64}'
        }

    def get_token_data(self):
        return {
            'grant_type': 'authorization_code',
            'code': self.code_for_token,
            'redirect_uri': self.redirect_uri
        }
    
    def set_code(self, code):
        self.code_for_token = code

    def get_authorization_url(self):
        auth_query = self.get_auth_data()

        r = requests.get(self.auth_url, params=auth_query)
        return r.url

    def set_token(self):
        # Define variables
        token_body = self.get_token_data()
        token_headers = self.get_token_headers()
        token_url = self.token_url
        # Request the token
        r = requests.post(token_url, data=token_body, headers=token_headers)
        # Validate the response
        if r.status_code not in range(200, 299):
            return False

        data  = r.json()
        now = datetime.datetime.now()
        self.access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_bearer_headers(self):
        return {
            "Authorization": f'Bearer {self.access_token}',
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_top_request_data(self, time_range, limit):
        return {
            'time_range': time_range,
            'limit': limit,
            'offset': 0
        }
        
    def get_top_tracks_ids(self, limit=10, time_range='medium_term'):
        endpoint = 'https://api.spotify.com/v1/me/top/tracks'
        headers = self.get_bearer_headers()
        data =  urlencode(self.get_top_request_data(time_range, limit))

        lookup_url = f"{endpoint}?{data}"

        r = requests.get(lookup_url, headers=headers)
        top_tracks = r.json()['items']

        ids = []
        names = []
        artists = []
        for idx, track in enumerate(top_tracks):
            ids.append(track['id'])
            names.append(track['name'])
            artists.append([])
            for artist in track['artists']:
                artists[idx].append(artist['name'])
        
        return ids, names, artists  

    def get_track_features(self, ids):
        endpoint = 'https://api.spotify.com/v1/audio-features'
        headers = self.get_bearer_headers()
        data = '%2C'.join(ids)

        lookup_url = f'{endpoint}?ids={data}'

        r = requests.get(lookup_url, headers=headers)

        return r.json()