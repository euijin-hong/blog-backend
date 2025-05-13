from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import app.schema.user as user_schema
import app.crud.user as user_crud
import app.model.model as model
from app.db.db import get_db


router = APIRouter(
    prefix="/user"
)

@router.post("/")
async def create_user(body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_crud.create_user(db, body)

@router.get("/", response_model=list[user_schema.User])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all_users(db)


@router.get("/user")
async def get_user():
    return {"user": "information"}

@router.get("/user/{user_id}")
async def get_user_info(user_id: int):
    return {"user information"}



@router.patch("/user")
async def update_user(user: user_schema.UserUpdate):
    return {"name": user.name,
            "email": user.email,
            "password": user.password}

