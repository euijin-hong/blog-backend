from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime

class UserBaseModel(BaseModel):
    email: EmailStr
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    

class UserCreate(UserBaseModel):
    name: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8, max_length=30, alias='password_hash')

class UserLogin(UserBaseModel):
    password: str

class User(UserBaseModel):
    id: int
    name: str = Field(...)
    created_at: datetime | None = Field(default=None)

class UserUpdate(UserBaseModel):
    name: str | None =Field(default=None, min_length=3, max_length=30)
    password: str | None = Field(default=None, min_length=8, max_length=30, alias='password_hash')

