from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.model.model import User
from app.schema.auth import LoginRequest
from app.db.db import get_db
from app.utils.security import verify_password
from app.utils.auth import create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, login_data: LoginRequest):
        query =(
            select(User)
            .where(User.email == login_data.email)
        )

        result: Result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not await verify_password(login_data.password, user.password):
            return None
        
        return user

    def create_user_token(self, user: User):
        token_data = {
            "email": user.email,
            "id": user.id
        }

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)