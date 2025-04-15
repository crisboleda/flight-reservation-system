from fastapi import FastAPI
from app.database import Base, engine, init_db
from app.routes import router
from app import models

app = FastAPI(
    title="Flights service",
    description="API para gestión de vuelos de la aerolínea",
    version="1.0",
)

app.include_router(router, prefix="/api/flights", tags=["Flights"])

init_db()
