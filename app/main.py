from app.core.config import settings
from app.services.base_service import BaseService
from fastapi import FastAPI
from app.api.v1.router import api_router

base = BaseService(settings, "endor-service")
app = base.app

# Mount all routes through the api_router
app.include_router(api_router, prefix=settings.API_V1_STR)


