from fastapi import APIRouter
from .endpoints import annotations, health

api_router = APIRouter()
api_router.include_router(annotations.router)
api_router.include_router(health.router) 