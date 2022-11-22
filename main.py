from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from routes.user.login import login

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
        "Message": "Codename - Neural",
        "Author" : "Farhan Aulianda"
    }
    
app.include_router(login)
