import httpx
import os
import uvicorn
from fastapi import FastAPI, Request
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/callback"

@app.get("/callback")
async def callback(request: Request):
    """Handling the Spotify redirect after autorization."""
    code = request.query_params.get("code")
    tg_id = request.query_params.get("state")

    if not code:
        return {"error": "Authorization failed"}

    # Changing the code for access_token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": SPOTIFY_CLIENT_ID,
                "client_secret": SPOTIFY_CLIENT_SECRET,
                },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

    token_data = response.json()

    # Check if we got the access_token
    if "access_token" in token_data:
        return {
            "message": "Authorization successful!",
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_in": token_data["expires_in"],
        }
    else:
        return {"error": "Failed to get access token", "details": token_data}

