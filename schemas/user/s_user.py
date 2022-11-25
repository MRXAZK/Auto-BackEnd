from typing import List, Union
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class User(BaseModel):
    id_user: int
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
