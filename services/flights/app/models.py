from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Aircraft(Base):
    __tablename__ = "aircrafts"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    registration_number = Column(String)
    total_seats = Column(Integer, nullable=False)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String)


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    origin_id = Column(Integer, ForeignKey("locations.id"))
    destination_id = Column(Integer, ForeignKey("locations.id"))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    price = Column(Float)

    aircraft_id = Column(Integer, ForeignKey("aircrafts.id"))

    origin = relationship("Location", foreign_keys=[origin_id])
    destination = relationship("Location", foreign_keys=[destination_id])
    aircraft = relationship("Aircraft")

    created_at = Column(DateTime, default=datetime.utcnow)
