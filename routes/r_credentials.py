from fastapi import Depends, APIRouter, Response, status, Security
from schemas.user.s_user import User
from schemas.credentials.s_credentials import ProfileCreate
from models.credentials.m_credentials import Profile as dataprofile
from config.database import conn
from functions.f_user import get_current_user
from functions.f_credentials import get_all_profile

credential = APIRouter()

@credential.get("/credentials/profile", tags=["Credentials"])
async def get_profile(current_user: User = Depends(get_current_user)):
    data =  get_all_profile(current_user.id_user)
    if data is None:
        response = Response(status_code=status.HTTP_404_NOT_FOUND)
        return {
            "status": response.status_code, 
            "message": "No Profile Found"
        }
    return data

@credential.post("/credentials/profile", response_model=ProfileCreate, tags=["Credentials"])
async def add_profile(current_user: User = Depends(get_current_user), pr: ProfileCreate = Depends()):
    query = dataprofile.insert().values(
                id_user = current_user.id_user,
                profile_name = pr.profile_name,
                access_id = pr.access_id,
                secret_access = pr.secret_access,
                date_created = pr.date_created
    )
    
    conn.execute(query)



