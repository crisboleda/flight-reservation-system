from fastapi import FastAPI
from app.routes import users_proxy
from app.routes import flights_proxy, reservations_proxy

app = FastAPI(
    title="API Gateway",
    description="API Gateway para la comunicación de los microservicios",
    version="1.0",
)

app.include_router(users_proxy.router, prefix="/api/users")
app.include_router(flights_proxy.router, prefix="/api/flights")
app.include_router(reservations_proxy.router, prefix="/api/reservations")
