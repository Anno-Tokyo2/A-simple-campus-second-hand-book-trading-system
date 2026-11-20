"""用户相关的 Pydantic schemas"""
from pydantic import BaseModel
from typing import Optional


class UserRegister(BaseModel):
    username: str
    password: str
    nickname: Optional[str] = ""
    school: Optional[str] = ""


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    nickname: str
    school: str
    avatar: str
    coin_balance: int
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    token: str
    user: UserResponse
