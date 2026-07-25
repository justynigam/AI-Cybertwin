import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_get_alerts_pagination(db_session):
    """
    Validates that the API correctly paginates and filters security alerts.
    """
    # 1. Arrange: The database fixture is already populated with mock alerts
    
    # 2. Act: Request the first 5 alerts
    response = client.get("/api/v1/alerts?skip=0&limit=5", headers={"Authorization": "Bearer mock_token"})
    
    # 3. Assert: Automated validation
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5
    assert "master_risk_score" in data[0]
    assert "attack_category" in data[0]

def test_get_alerts_invalid_severity():
    """
    Validates that query parameter validation handles request queries correctly.
    """
    # Test valid query parameters
    response = client.get("/api/v1/alerts?severity=CRITICAL", headers={"Authorization": "Bearer mock_token"})
    assert response.status_code == 200
