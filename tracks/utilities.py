feature_list = ['name', 
            'track_id',
            'artist',
            'uri',
            'danceability',
            'valence',
            'energy',
            'tempo',
            'loudness',
            'speechiness',
            'instrumentalness',
            'liveness',
            'acousticness',
            'key',
            'mode',
            'time_signature'
 ]

def clean_json(features, names, artists):
    new_features = []
    for idx, feature in enumerate(features):
        feature['name'] = names[idx]
        feature['artist'] = ''
        for artist in artists[idx]:
            if feature['artist'] == '':
                feature['artist'] = artist
            else:
                feature['artist'] += f', {artist}'
        
        feature['track_id'] = feature['id']
        feature.pop('id')

        new_features.append({key:value for (key, value) in feature.items() if key in feature_list})

    return new_features

from tracks.models import Track
def create_track(tracks):
    for track in tracks:
        Track.objects.create(**track)
