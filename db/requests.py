import httpx
import logging

from db.models import async_session
from db.models import User
from sqlalchemy import select

from endpoints import TOKEN_URL, MAIN_ENDPOINT, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, get_tops_link, get_rec_link

logger = logging.getLogger(__name__)


async def set_user(tg_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, name=name))
            await session.commit()


async def set_tokens(tg_id, access_token, refresh_token):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.access_token = access_token
            user.refresh_token = refresh_token
        else:
            session.add(User(tg_id=tg_id, access_token=access_token, refresh_token=refresh_token))
        await session.commit()


async def token_endpoint_conn(url, data, headers):
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            return response.json()


async def refresh_access_token(tg_id) -> str|None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user or not user.refresh_token:
            return None

        token_data = await token_endpoint_conn(
            url=TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": user.refresh_token,
                "client_id": SPOTIFY_CLIENT_ID,
                "client_secret": SPOTIFY_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if "access_token" in token_data:
            user.access_token = token_data["access_token"]
            await session.commit()
            return user.access_token
        else:
            return None


async def get_valid_access_token(tg_id) -> str|None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user or not user.access_token:
            return None

        # Check if the token is working (by test request)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                MAIN_ENDPOINT,
                headers={"Authorization": f"Bearer {user.access_token}"}
                )

        if response.status_code == 200:
            return user.access_token  # The token is valid

        elif response.status_code == 401:
            return await refresh_access_token(tg_id)  # The token is outdated and be refreshed

        return None  # Error


async def get_charts(tg_id, entity, time_range, limit):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user or not user.access_token:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(
                get_tops_link(entity, time_range, limit),
                headers={"Authorization": f"Bearer {user.access_token}"}
            )

        if response.status_code == 200:
            return response.json()

        return None  # Error


async def get_recommendations(tg_id, seed_artists=None, seed_tracks=None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user or not user.access_token:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(
                get_rec_link(seed_artists, seed_tracks),
                headers={"Authorization": f"Bearer {user.access_token}"}
            )

        if response.status_code == 200:
            return response.json()

        return None  # Error



async def get_admins():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.is_admin.is_(True)))
        return result.scalars().all()