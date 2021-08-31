from django.db import models

# Create your models here.
class Track(models.Model):
    # Basic Info
    name             = models.TextField()
    artist           = models.TextField()
    track_id         = models.TextField()
    uri              = models.TextField()
    # Audio Feature 
    danceability     = models.FloatField()
    valence          = models.FloatField()
    energy           = models.FloatField()
    tempo            = models.FloatField()
    loudness         = models.FloatField()
    speechiness      = models.FloatField()
    instrumentalness = models.FloatField()
    liveness         = models.FloatField()
    acousticness     = models.FloatField()
    key              = models.FloatField()
    mode             = models.FloatField()
    time_signature   = models.FloatField()
