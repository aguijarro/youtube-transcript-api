import pytest
from fastapi.testclient import TestClient
from app.main import app
from motor.motor_asyncio import AsyncIOMotorClient
from unittest.mock import Mock

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_db():
    # Mock MongoDB client
    return Mock(spec=AsyncIOMotorClient)
