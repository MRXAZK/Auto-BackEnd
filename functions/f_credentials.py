
from config.database import conn
from fastapi import Response

from models.credentials.m_credentials import Profile as dataprofile
from models.user.m_user import User as datauser

from schemas.credentials.s_credentials import ProfileCreate

def get_all_profile(id_user: int):
    query = dataprofile.select().join(dataprofile, dataprofile.c.id_user == datauser.c.id_user).where(datauser.c.id_user == id_user)
    data = conn.execute(query).fetchall()
    if not data:
        return None
    return data  


    
    
    
    
    
    
        
    

