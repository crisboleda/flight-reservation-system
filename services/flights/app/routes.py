from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import and_

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("/search", response_model=List[schemas.FlightResponse])
def search_flights(
    origin_id: Optional[int] = Query(None),
    destination_id: Optional[int] = Query(None),
    departure_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    filters = []
    if origin_id:
        filters.append(models.Flight.origin_id == origin_id)
        if destination_id:
            filters.append(models.Flight.destination_id == destination_id)
            if departure_date:
                filters.append(
                    models.Flight.departure_time.between(
                        datetime.combine(departure_date, datetime.min.time()),
                        datetime.combine(departure_date, datetime.max.time()),
                    )
                )

    flights = db.query(models.Flight).filter(and_(*filters)).all()
    return flights


@router.post("/", response_model=schemas.FlightResponse)
def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    for model_class, field_id in [
        (models.Location, flight.origin_id),
        (models.Location, flight.destination_id),
        (models.Aircraft, flight.aircraft_id),
    ]:
        if not db.query(model_class).filter(model_class.id == field_id).first():
            raise HTTPException(
                status_code=404,
                detail=f"{model_class.__name__} not found with id={field_id}",
            )

    db_flight = models.Flight(**flight.model_dump())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


@router.get("/", response_model=list[schemas.FlightResponse])
def get_all_flights(db: Session = Depends(get_db)):
    return db.query(models.Flight).all()


@router.get("/{flight_id}", response_model=schemas.FlightResponse)
def get_flight(flight_id: int, db: Session = Depends(get_db)):
    flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight
