from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from app.utils.flights import get_flight

router = APIRouter()


@router.post("/", response_model=schemas.ReservationResponse)
def create_reservation(
    reservation: schemas.ReservationCreate, db: Session = Depends(get_db)
):
    flight_data = get_flight(reservation.flight_id)
    total_seats = flight_data["aircraft"]["total_seats"]

    booked = (
        db.query(models.Reservation).filter_by(flight_id=reservation.flight_id).count()
    )

    if booked >= total_seats:
        raise HTTPException(
            status_code=400, detail="No hay asientos disponibles para este vuelo"
        )

    new_reservation = models.Reservation(**reservation.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return schemas.ReservationResponse(
        id=new_reservation.id,
        user_id=new_reservation.user_id,
        flight_id=new_reservation.flight_id,
        created_at=new_reservation.created_at,
        flight=flight_data,
    )


@router.get("/user/{user_id}", response_model=list[schemas.Reservation])
def get_user_reservations(user_id: str, db: Session = Depends(get_db)):
    return db.query(models.Reservation).filter_by(user_id=user_id).all()


@router.delete("/{reservation_id}")
def cancel_reservation(reservation_id: str, db: Session = Depends(get_db)):
    res = db.query(models.Reservation).filter_by(id=reservation_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(res)
    db.commit()
    return {"detail": "Reservation cancelled"}
