import json
from pathlib import Path
from sqlalchemy.orm import Session
from app import models
from datetime import datetime


def load_seed_data(db: Session):
    if db.query(models.Flight).first():
        return

    path = Path(__file__).resolve().parent / "seed_data.json"
    with open(path) as f:
        data = json.load(f)

    location_map = {}
    for loc in data["locations"]:
        location = models.Location(**loc)
        db.add(location)
        db.flush()
        location_map[loc["code"]] = location.id

    aircraft_map = {}
    for ac in data["aircrafts"]:
        aircraft = models.Aircraft(**ac)
        db.add(aircraft)
        db.flush()
        aircraft_map[ac["registration_number"]] = aircraft.id

    for flight in data["flights"]:
        departure_time = datetime.fromisoformat(flight["departure_time"])
        arrival_time = datetime.fromisoformat(flight["arrival_time"])

        db.add(
            models.Flight(
                origin_id=location_map[flight["origin_code"]],
                destination_id=location_map[flight["destination_code"]],
                departure_time=departure_time,
                arrival_time=arrival_time,
                price=flight["price"],
                aircraft_id=aircraft_map[flight["aircraft_registration"]],
            )
        )

    db.commit()
