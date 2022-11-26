from typing import List, Union
from pydantic import BaseModel
from datetime import date


class ProfileCreate(BaseModel):
    id_user: int
    profile_name : str
    access_id : str
    secret_access : str
    date_created: date

