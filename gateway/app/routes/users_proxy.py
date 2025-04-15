from fastapi import APIRouter, Request
import requests
from app.config import USERS_SERVICE_URL

router = APIRouter()


@router.post("/register")
def register_user(request: Request):
    body = request.json()
    response = requests.post(f"{USERS_SERVICE_URL}/register", json=body)
    return response.json()


@router.post("/login")
def login_user(request: Request):
    body = request.json()
    response = requests.post(f"{USERS_SERVICE_URL}/login", json=body)
    return response.json()
