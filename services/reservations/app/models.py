import uuid
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Reservation(Base):

    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    flight_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
