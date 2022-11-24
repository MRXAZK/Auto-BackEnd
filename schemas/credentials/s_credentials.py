from typing import List, Union
from fastapi import Depends, HTTPException, Security, status, Response
from fastapi.security import (
    SecurityScopes,
)
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from models.user.m_user import User as datauser
from schemas.user.s_user import get_current_user
from functions.f_credentials import get_all_credentials

SECRET_KEY = "9469d55b26db76923bdf184d03ecdcea600434f28b198df2ae08d2eaecfa6340"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class Credentials(BaseModel):
    id_user: int
    profile_name: str
    access_id: Union[str, None] = None
    secret_access: Union[str, None] = None

class UserCreate(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    password: Union[str, None] = None
    confirm_password: Union[str, None] = None
    disabled: Union[bool, None] = None



class UserInDB(Credentials):
    hashed_password: str


async def create_profile(
    current_user: Credentials = Security(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_profile(current_user: Credentials = Security(get_current_user)):
        
    data = get_all_credentials(current_user.id_user)
    