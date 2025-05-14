from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.engine import Result

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db
from app.utils.auth import verify_token
from app.model.model import User

bearer_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), 
                     db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, 
                            detail="The user is not authorized",
                            headers={"WWW-Authenticate": "bearer"})
    
    email = payload.get("email")
    if email is None:
        raise HTTPException(status_code=401, 
                            detail="The user is not authorized",
                            headers={"WWW-Authenticate": "Bearer"})
    
    query = (
        select(User)
        .where(User.email == email)
    )
    result: Result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, 
                            detail="Cannot find the user.",
                            headers={"WWW-Authenticate": "Bearer"})
    
    return user