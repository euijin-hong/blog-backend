from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    if pwd_context.verify(plain_password, hashed_password):
        print("password verified!!")
    else: print("PASSWORD NOT MATCH!!!")
    return pwd_context.verify(plain_password, hashed_password)