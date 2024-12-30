# Routes aggregation

from fastapi import APIRouter
from app.api.v1.endpoints import health, transcript

api_router = APIRouter()

# Add health endpoint without additional prefix
api_router.include_router(health.router, tags=["health"])
api_router.include_router(transcript.router, prefix="/transcript", tags=["transcript"]) 