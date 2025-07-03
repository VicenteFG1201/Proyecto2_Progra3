from fastapi import FastAPI
from api.controllers import client_routes, order_routes, report_routes, info_routes

app = FastAPI(
    title="Drone Simulation API",
    description="API RESTful para consultar y controlar el sistema de rutas autónomas con drones.",
    version="2.0"
)

app.include_router(client_routes.router, prefix="/clients")
app.include_router(order_routes.router, prefix="/orders")
app.include_router(report_routes.router, prefix="/reports")
app.include_router(info_routes.router, prefix="/info/reports")