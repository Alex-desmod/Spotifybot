from fastapi import FastAPI, Request

import db.requests as rq

from endpoints import TOKEN_URL, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI

app = FastAPI()

@app.get("/callback")
async def callback(request: Request):
    """Handling the Spotify redirect after autorization."""
    code = request.query_params.get("code")
    tg_id = request.query_params.get("state")

    if not code:
        return {"error": "Authorization failed"}

    # Changing the code for access_token
    token_data = await rq.token_endpoint_conn(url=TOKEN_URL,
                                        data={
                                            "grant_type": "authorization_code",
                                            "code": code,
                                            "redirect_uri": REDIRECT_URI,
                                            "client_id": SPOTIFY_CLIENT_ID,
                                            "client_secret": SPOTIFY_CLIENT_SECRET,
                                        },
                                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                                        )

    # Check if we got the access_token
    if "access_token" in token_data:
        await rq.set_tokens(tg_id, access_token=token_data["access_token"], refresh_token=token_data["refresh_token"])
        return {"message": "Tokens saved successfully!"}
    else:
        return {"error": "Failed to get access token"}

