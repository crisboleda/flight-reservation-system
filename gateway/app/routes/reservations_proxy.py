from fastapi import APIRouter, Depends, HTTPException, Request
from auth import verify_token
from app.config import RESERVATIONS_SERVICE_URL
import requests

router = APIRouter()


@router.get("/")
def get_user_reservations(user=Depends(verify_token)):
    try:
        response = requests.get(
            f"{RESERVATIONS_SERVICE_URL}/api/reservations/user/{user['id']}"
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code, detail="Error to obtain reservations"
            )
    except requests.RequestException:
        raise HTTPException(
            status_code=500, detail="Error to connect with reservations-service"
        )

@router.post("/")
def get_create_reservation(data: dict, user=Depends(verify_token)):
    try:
        data["user_id"] = user.get("id")
        response = requests.post(
            f"{RESERVATIONS_SERVICE_URL}/api/reservations/", json=data
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code, detail="Error to create reservation"
            )
    except requests.RequestException:
        raise HTTPException(
            status_code=500, detail="Error to connect with reservations-service"
        )
