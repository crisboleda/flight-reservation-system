from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from auth import verify_token
from app.config import FLIGHTS_SERVICE_URL
from datetime import date
import requests

router = APIRouter()


@router.get("/search")
def search_flights(
    origin_id: Optional[int] = Query(None),
    destination_id: Optional[int] = Query(None),
    departure_date: Optional[date] = Query(None),
    user=Depends(verify_token),
):
    try:
        response = requests.get(
            f"{FLIGHTS_SERVICE_URL}/api/flights/search?origin_id={origin_id}&destination_id={destination_id}&departure_date={departure_date}"
        )
        if response.status_code == 200:
            return response.json()

        raise HTTPException(
            status_code=response.status_code, detail="Error to obtain flights"
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=500, detail="Error to connect with flights-service"
        )


@router.get("/{flight_id}")
def get_flight_by_id(flight_id: int, user=Depends(verify_token)):
    try:
        response = requests.get(f"{FLIGHTS_SERVICE_URL}/api/flights/{flight_id}")
        if response.status_code == 200:
            return response.json()

        raise HTTPException(
            status_code=response.status_code, detail="Error to obtain flight by ID"
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=500, detail="Error to connect with flights-service"
        )
