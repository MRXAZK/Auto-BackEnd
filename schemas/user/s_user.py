from typing import List, Union
from fastapi import Depends, HTTPException, Security, status, Response
from fastapi.security import (
    SecurityScopes,
)
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from models.user.m_user import User as datauser
from functions.f_user import oauth2_scheme, get_user, authenticate_user, create_access_token, check_exist, add_user

SECRET_KEY = "9469d55b26db76923bdf184d03ecdcea600434f28b198df2ae08d2eaecfa6340"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserCreate(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    password: Union[str, None] = None
    confirm_password: Union[str, None] = None
    disabled: Union[bool, None] = None



class UserInDB(User):
    hashed_password: str


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["me"])
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def create_user(usr: UserCreate, response: Response):
        
    username = check_exist(usr.username)
    
    if username is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": response.status_code, 
            "message": "Username Already Exists"
        }
    else:
        if usr.password != usr.confirm_password:
            response.status_code = status.HTTP_409_CONFLICT
            return {
                "status": response.status_code, 
                "message": "Password and Confirm Password not match"
            }
            
        add_user(usr.username, usr.password, usr.email, usr.full_name)
        response = {
            "message" : f"Success add new data data",
        }
        return response         
        
    