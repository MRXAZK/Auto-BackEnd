from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, HTTPException, Security, status, Response
from fastapi import Response, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.database import conn
from pydantic import ValidationError
from models.user.m_user import User as datauser
from schemas.user.s_user import UserCreate, User, UserInDB, Token, TokenData

from fastapi.security import (
    SecurityScopes,
)
from jose import JWTError, jwt


SECRET_KEY = "9469d55b26db76923bdf184d03ecdcea600434f28b198df2ae08d2eaecfa6340"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    # get data from database
    query = datauser.select().filter(datauser.c.username == username)
    data = conn.execute(query).fetchone()
    if data is None:
        return None
    user_dict = dict(data)
    user = UserInDB(**user_dict)
    return user

def add_user(username: str, password: str, email: str, full_name: str):
    query = datauser.insert().values(
        username = username,
        full_name = full_name,
        email = email,
        hashed_password = get_password_hash(password),
        disabled = False
    )   
    conn.execute(query)
    return True

def check_exist(username: str):
    # get data from database
    query = datauser.select().filter(datauser.c.username == username)
    data = conn.execute(query).fetchone()
    if data is None:
        return None
    return data

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



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
    current_user: User = Security(get_current_user)
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
      
        
    
