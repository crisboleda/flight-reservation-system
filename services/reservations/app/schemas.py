from pydantic import BaseModel
from datetime import datetime


class ReservationCreate(BaseModel):
    user_id: int
    flight_id: int


class Reservation(BaseModel):
    id: int
    user_id: int
    flight_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FlightData(BaseModel):
    id: int
    origin: dict
    destination: dict
    departure_time: datetime
    arrival_time: datetime
    price: float
    aircraft: dict

    class Config:
        from_attributes = True


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    flight_id: int
    created_at: datetime
    flight: FlightData

    class Config:
        from_attributes = True
