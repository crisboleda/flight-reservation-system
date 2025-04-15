import pytest
from datetime import datetime, timedelta
from app import models


@pytest.fixture
def sample_data(db_session):
    destination = models.Location(name="Los Angeles", code="LAX")
    origin = models.Location(name="New York", code="JFK")
    db_session.add_all([origin, destination])
    db_session.commit()
    db_session.refresh(origin)
    db_session.refresh(destination)

    aircraft = models.Aircraft(
        model="Boeing 737", registration_number="N12345", total_seats=180
    )
    db_session.add(aircraft)
    db_session.commit()
    db_session.refresh(aircraft)

    return {
        "origin_id": origin.id,
        "destination_id": destination.id,
        "aircraft_id": aircraft.id,
    }


def test_create_and_get_flight(client, sample_data):
    flight_data = {
        "origin_id": sample_data["origin_id"],
        "destination_id": sample_data["destination_id"],
        "departure_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "arrival_time": (datetime.now() + timedelta(days=1, hours=5)).isoformat(),
        "price": 199.99,
        "aircraft_id": sample_data["aircraft_id"],
    }

    response = client.post("/api/flights/", json=flight_data)
    assert response.status_code == 200
    flight = response.json()
    assert flight["origin"]["code"] == "JFK"
    assert flight["destination"]["code"] == "LAX"
    assert flight["aircraft"]["model"] == "Boeing 737"

    response = client.get(f"/api/flights/{flight['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == flight["id"]
