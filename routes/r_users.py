from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from schemas.user.s_user import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, get_current_user, create_user
from schemas.user.s_user import User, Token

login = APIRouter()


@login.post("/token", response_model=Token, tags=["Token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@login.post("/users/create/", description="Add Data", tags=["Sign Up"])
async def create_data(current_user: User = Depends(create_user)):
    return current_user


@login.get("/users/me/", response_model=User, tags=["Login"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@login.get("/users/me/items/", tags=["Login"])
async def read_own_items(
    current_user: User = Security(get_current_active_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@login.get("/status/", tags=["Login"])
async def read_system_status(current_user: User = Depends(get_current_user)):
    return {"status": "ok"}



