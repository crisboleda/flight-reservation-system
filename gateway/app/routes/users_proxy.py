from fastapi import APIRouter, Request
import requests
from app.config import USERS_SERVICE_URL

router = APIRouter()


@router.post("/register")
def register_user(
    data: dict = {"name": "Example", "email": "user@example.com", "password": "string"}
):
    response = requests.post(f"{USERS_SERVICE_URL}/api/users/register", json=data)
    return response.json()


@router.post("/login")
def login_user(data: dict = {"email": "user@example.com", "password": "string"}):
    response = requests.post(f"{USERS_SERVICE_URL}/api/users/login", json=data)
    return response.json()
