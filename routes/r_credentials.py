from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from schemas.credentials.s_credentials import create_profile, get_profile
from schemas.credentials.s_credentials import Credentials

credential = APIRouter()


@credential.post("/credentials/profile", description="Add Data", tags=["Credentials"])
async def add_credentials(current_user: Credentials = Depends(create_profile)):
    return current_user


@credential.get("/credentials/profile", response_model=Credentials, tags=["Credentials"])
async def get_credentials(current_user: Credentials = Depends(get_profile)):
    return current_user


