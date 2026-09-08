from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import authenticate_user, users

class LoginRequest(BaseModel):
    username: str
    password: str
app = FastAPI()
@app.post("/login")
def login(login_data: LoginRequest):
    valid_login = authenticate_user(
        users, login_data.username, login_data.password
    )
    if valid_login:
        return {
            "authenticated" : True,
            "username" : login_data.username,
            "role" : users[login_data.username]["role"]
        }
    else:
        raise HTTPException(
            status_code= 401, 
            detail= "Invalid Credentials"
        )
        







@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

    