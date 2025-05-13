import app.schema.user as user_schema
import app.model.model as model

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result


async def create_user(db: AsyncSession, userinfo: user_schema.UserCreate) -> model.User:
    new_user = model.User(**userinfo.model_dump())
    db.add(new_user)
    await db.commit()
    return new_user

async def get_all_users(db: AsyncSession) -> list[user_schema.User]:
    result: Result = await db.execute(
        select(model.User)
    )
    users = result.scalars().all()
    return [user_schema.User(
        id = user.id,
        name = user.name,
        email = user.email,
        created_at = user.created_at
    ) for user in users]