from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from pages.spotify_class import SpotifyApi
from decouple import config
from tracks.utilities import clean_json, create_track

# Init the Spotify API
client_id = config('SPOTIPY_CLIENT_ID')
client_secret = config('SPOTIPY_CLIENT_SECRET')
redirect_uri = config('SPOTIPY_REDIRECT_URI')
scopes = [
    'user-read-playback-state',
    'user-read-currently-playing',
    'user-read-email',
    'user-read-private',
    'playlist-read-collaborative',
    'playlist-read-private',
    'user-library-read',
    'user-top-read',
    'user-read-playback-position',
    'user-read-recently-played',
    'user-follow-read',
]

client = SpotifyApi(client_id, client_secret, redirect_uri,'user-top-read')

# Create your views here.
def home_view(req):
    context = {}
    return render(req, 'index.html', context)

def login_view(req):
    auth_url = client.get_authorization_url()
    
    return redirect(auth_url)


def callback_view(req):
    # Get the code
    client.set_code(req.GET.get('code', ''))
    # Get the token
    validate_token = client.set_token()

    if validate_token:
        access_token = client.access_token
    else:
        raise Exception('Oh no, something went wrong')

    # Extract features from top 50 tracks for a user
    top_tracks_ids, top_tracks_names, top_tracks_artists = client.get_top_tracks_ids(limit=50)
    track_features = client.get_track_features(top_tracks_ids)['audio_features']
    complete_tracks = clean_json(track_features, top_tracks_names, top_tracks_artists)

    # Save in the database
    print('--------------')
    create_track(complete_tracks)
    print('--------------')

    return HttpResponse('Hi there!')