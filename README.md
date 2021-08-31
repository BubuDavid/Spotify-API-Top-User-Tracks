# Django app with Spotify API
I built a simple Django app that grabs your top 50 spotify songs and save them on a sqlite3 database, this will be used for train a ML model that can tell your personality type based on your likes.

# Requirements
- python 3.0+
- Django 3.0+
- [A Spotify Developer account](https://developer.spotify.com/) (Is free)
- A Spotify App

# Setup
To get ready just follow the instructions.

1. Clone the project repository:
```bash
git clone https://github.com/BubuDavid/Spotify-API-Top-User-Tracks.git

cd Spotify-Api-Top-User-Tracks
```

2. You can create an environment with 
```bash
virtualenv -p python .
```
and activate it with:
```bash
# Windows
Script/activate.bat
# IOS
source spotify-top/bin/activate
```
or with conda by typing
```bash
conda create -n spotify-top
```

and activate it whith
```bash
conda activate spotify-top
```

3. Install the requirements
```bash
(pose-estimation)$ pip install -r requirements.txt
```

4. Remember to set your client_id and client_secret from you spotify app, you can use enviroment variables or a .env document. 
If you do not know how to create an app, follow this [tutorial](https://developer.spotify.com/documentation/general/guides/app-settings/).

5. Set your redirect_uri to _http://localhost:8888/callback_ inside your app settings on spotify developer.

5. And to run the app you can do
```bash
python manage.py runserver 8888
```