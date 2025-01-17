from fastapi import APIRouter

from app.api.endpoints import schedule, routes

api_router = APIRouter()

api_router.include_router(schedule.router, tags=["schedule"], prefix="/schedule")
api_router.include_router(routes.router, tags=["routes"], prefix="/routes")