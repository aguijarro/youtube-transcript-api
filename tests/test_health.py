from fastapi.testclient import TestClient

def test_health_check(test_app: TestClient):
    response = test_app.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy_service"}
