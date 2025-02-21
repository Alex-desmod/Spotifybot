from app.db.models import async_session
from app.db.models import User
from sqlalchemy import select


async def set_user(tg_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, name=name))
            await session.commit()

async def get_admins():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.is_admin.is_(True)))
        return result.scalars().all()