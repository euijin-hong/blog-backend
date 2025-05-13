from fastapi import APIRouter, HTTPException



router = APIRouter()


@router.get("/auth/login")
async def log_in():
    return {"login": "information"}

@router.get("/auth/signup")
async def sign_up():
    return {"sign up": "information"}

@router.get("/auth/logout")
async def log_out():
    return{"user": "logged out"}