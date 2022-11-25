
from config.database import conn

from models.credentials.m_credentials import Profile as dataprofile
from models.user.m_user import User as datauser

def get_all_credentials(id_user: int):
    query = dataprofile.select().join(dataprofile, dataprofile.c.id_user == datauser.c.id_user).where(datauser.c.id_user == id_user)
    data = conn.execute(query).fetchall()
    if not data:
        return None
    return data  
    

