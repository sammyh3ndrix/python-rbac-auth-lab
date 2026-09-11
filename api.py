from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import authenticate_user, users
import os 
import sentry_sdk
from main import logger
import logging

journald_module_available = False
try:
    from systemd import journal
    journald_module_available = True
except ModuleNotFoundError:
    pass

if journald_module_available:
    journal_handler = journal.JournalHandler()
    logger.addHandler(journal_handler)
    logger.setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


sentry_dsn = os.environ.get("SENTRY_DSN")

if sentry_dsn:
    sentry_sdk.init(
        dsn = sentry_dsn
    )

    






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