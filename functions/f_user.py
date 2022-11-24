from datetime import datetime, timedelta
from typing import Union
from fastapi import Response, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.database import conn
from models.user.m_user import User as datauser
import schemas.user.s_user as schema


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
    query = datauser.select()
    data = conn.execute(query).fetchone()
    if data is None:
        return None
    user_dict = dict(data)
    user = schema.UserInDB(**user_dict)
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
    data = datauser.select().order_by(datauser.c.id_user.desc())
    response = {
        "message" : f"Success add new data data", "data": conn.execute(data).fetchone()
    }
    return response

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
    encoded_jwt = jwt.encode(to_encode, schema.SECRET_KEY, algorithm=schema.ALGORITHM)
    return encoded_jwt
