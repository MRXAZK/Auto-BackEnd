from datetime import datetime, timedelta
from typing import Union
from fastapi import Response, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.database import conn
from models.credentials.m_credentials import Profile as dataprofile
import schemas.credentials.s_credentials as schema


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
    query = dataprofile.select()
    data = conn.execute(query).fetchone()
    if data is None:
        return None
    user_dict = dict(data)
    user = schema.UserInDB(**user_dict)
    return user

def add_user(username: str, password: str, email: str, full_name: str):
    query = dataprofile.insert().values(
        username = username,
        full_name = full_name,
        email = email,
        hashed_password = get_password_hash(password),
        disabled = False
    )   
    conn.execute(query)
    return True

def get_all_credentials(id_user: int):
    # get data from database
    query = dataprofile.select().filter(dataprofile.c.id_user == id_user)
    data = conn.execute(query).fetchone()
    if data is None:
        return None
    return data

