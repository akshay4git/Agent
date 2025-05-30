from fastapi import APIRouter
from app.api.endpoints import chat, metrics, devices, data

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(data.router, prefix="/sample-data",tags=["sample data"])