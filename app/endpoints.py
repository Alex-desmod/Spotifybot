import os

from app.web_server import SPOTIFY_CLIENT_ID,REDIRECT_URI


SCOPES = "user-top-read user-read-recently-played"
AUTH_URL = "https://accounts.spotify.com/authorize"

def get_auth_link(tg_id):
    return (f"{AUTH_URL}?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
            f"&state={tg_id}&scope={SCOPES}")

