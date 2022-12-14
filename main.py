from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from routes.r_users import login
from routes.r_credentials import credential


app = FastAPI()

def cors_headers(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
        )
    return app

@app.get("/", tags=["Root"])
async def root():
    return {
        "Message": "Auto - BackEnd",
        "Author" : "Farhan Aulianda"
    }
    
app.include_router(login)
app.include_router(credential)

