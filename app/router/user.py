from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.user import User, UserCreate, UserUpdate
import app.crud.user as user_crud
import app.model.model as model
from app.services.auth_service import AuthService, get_auth_service
from app.schema.auth import TokenResponse, LoginRequest, RefreshRequest
from app.db.db import get_db
from app.services.user_service import get_user_service, UserService
from app.services.token_service import TokenService
from app.utils.auth import get_token_expiry, verify_token


bearer_scheme = HTTPBearer()

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


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials

    token_expiry = get_token_expiry(token)
    TokenService.blacklist_token(token, token_expiry)

    return {"Message": "Successfully logged out."}

@router.post(
    "/refresh",
    response_model=TokenResponse
)
async def refresh_token(refresh_data: RefreshRequest,
                        auth_service: AuthService = Depends(get_auth_service)):
    token = await auth_service.refresh_access_token(refresh_data.refresh_token)

    if not token:
        raise HTTPException(status_code=401, 
                            detail="User detail is not valid",
                            headers={"WWW-Authenticate": "Bearer"})
    
    token["refresh_token"] = refresh_data.refresh_token

    return token

@router.post("/logout-all")
async def logout_all_sesssion(
    credentials: HTTPAuthorizationCredentials=Depends(bearer_scheme)
):
    token = credentials.credentials
    token_expiry = get_token_expiry(token)
    TokenService.blacklist_token(token, token_expiry)

    user_email=verify_token(token).get("email")
    TokenService.revoke_refresh_token(user_email)

    return {"Message": "Logged out from all devices"}