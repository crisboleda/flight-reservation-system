from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LocationBase(BaseModel):
    name: str
    code: str


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AircraftBase(BaseModel):
    model: str
    registration_number: str
    total_seats: int


class AircraftResponse(AircraftBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FlightCreate(BaseModel):
    origin_id: int
    destination_id: int
    departure_time: datetime
    arrival_time: datetime
    price: float
    aircraft_id: int


class FlightResponse(FlightCreate):
    id: int
    origin: LocationResponse
    destination: LocationResponse
    aircraft: AircraftResponse

    model_config = ConfigDict(from_attributes=True)
