import requests
from fastapi import HTTPException


FLIGHTS_SERVICE_URL = "http://flights-service:8000/api/flights"


def get_flight(flight_id: str) -> dict:
    """Consulta el microservicio de flights y obtiene
    la información de un vuelo específico."""
    response = requests.get(f"{FLIGHTS_SERVICE_URL}/{flight_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Flight Not Found")
    return response.json()
