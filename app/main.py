from app.core.config import settings
from app.api.v1.endpoints import health, test
from app.services.base_service import BaseService

base = BaseService(settings, "endor-service")
app = base.app

app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])
app.include_router(test.router, prefix=f"{settings.API_V1_STR}/test", tags=["test"])


