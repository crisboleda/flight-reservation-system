import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.seed_loader import load_seed_data

ENV = os.getenv("ENV", "dev")

if ENV == "test":
    DATABASE_URL = "sqlite:///./tests/test.db"
else:
    DATABASE_URL = "sqlite:///./flights.db"

engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    load_seed_data(db)
    db.close()
