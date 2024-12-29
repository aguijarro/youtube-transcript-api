import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import Settings, get_settings


def get_settings_override():
    return Settings(
        PROJECT_NAME="FastAPI Test App",
        DEBUG=True,
        MONGODB_URL="mongodb://endor_python_mongodb:27017",
        MONGODB_DB_NAME="endor_python_test",
        ALLOWED_ORIGINS="http://localhost:3000",
        ENVIRONMENT="test"
    )


@pytest.fixture(scope="module")
def test_app():
    # set up
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        # testing
        yield test_client
    # tear down
    app.dependency_overrides = {}
