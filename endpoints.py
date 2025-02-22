import os
from dotenv import load_dotenv

load_dotenv()


SCOPES = "user-top-read user-read-recently-played user-read-private"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
MAIN_ENDPOINT = "https://api.spotify.com/v1/me"

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/callback"

def get_auth_link(tg_id):
    return (f"{AUTH_URL}?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
            f"&state={tg_id}&scope={SCOPES}")

def get_tops_link(entity, time_range, limit):
    return f"{MAIN_ENDPOINT}/top/{entity}?time_range={time_range}&limit={limit}&offset=0"

def get_rec_link(seed_artists=None, seed_tracks=None):
    url = "https://api.spotify.com/v1/recommendations?"
    if seed_artists:
        return f"{url}seed_artists={seed_artists}&limit=10"
    if seed_tracks:
        return f"{url}seed_tracks={seed_tracks}&limit=10"
    return None

