from fastapi import FastAPI
from . import models
from .database import engine
from .routes import router

app = FastAPI(
    title="Users service",
    description="API para gestión de usuarios de la aerolínea",
    version="1.0",
)

app.include_router(router, prefix="/api/users", tags=["Users"])

models.Base.metadata.create_all(bind=engine)
