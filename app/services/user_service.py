from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from app.db.db import get_db
from app.utils.security import get_password_hash
import app.model.model as model

import app.schema.user as user_schema

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: user_schema.UserCreate):
        hashed_password = await get_password_hash(user.password)
        db_user = model.User(
            email=user.email,
            name=user.name,
            password=hashed_password
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user
    
    async def get_user_by_email(self, email: str):
        query=(
            select(model.User)
            .where(model.User.email == email)
        )
        result: Result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user
    
async def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)