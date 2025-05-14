from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.user import User, UserCreate, UserUpdate
import app.crud.user as user_crud
import app.model.model as model
from app.services.auth_service import AuthService, get_auth_service
from app.schema.auth import TokenResponse, LoginRequest
from app.db.db import get_db
from app.services.user_service import get_user_service, UserService


router = APIRouter(
    prefix="/user"
)

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, 
                        user_service: UserService = Depends(get_user_service)):
    existed_user_email = await user_service.get_user_by_email(user.email)
    if existed_user_email:
        raise HTTPException(status_code=409, detail="The email already exists.")
    
    return await user_service.create_user(user)
    
@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, 
                auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.authenticate_user(login_data)

    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed",headers={"WWW-Authenticate": "Bearer"})
    
    token_data = auth_service.create_user_token(user)

    return token_data


@router.get("/", response_model=list[User])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all_users(db)
