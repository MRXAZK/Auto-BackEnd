from fastapi import Depends, APIRouter, Response, status
from schemas.user.s_user import User
from functions.f_user import get_current_user
from functions.f_credentials import get_all_credentials

credential = APIRouter()

@credential.get("/credentials/profile", tags=["Credentials"])
async def get_credentials(current_user: User = Depends(get_current_user)):
    data =  get_all_credentials(current_user.id_user)
    if data is None:
        response = Response(status_code=status.HTTP_404_NOT_FOUND)
        return {
            "status": response.status_code, 
            "message": "No Profile Found"
        }
    return data



