import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_post_ingest_event():
    payload = {
        "event_id": str(uuid.uuid4()),
        "user_id": "usr-test-100",
        "device_id": "dev-test-200",
        "event_type": "AUTHENTICATION",
        "action": "LOGIN_SUCCESS",
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": "192.168.1.50",
        "geo_location": "New York",
        "is_attack": False,
        "attack_category": "None"
    }

    response = client.post("/api/v1/ingest", json=payload, headers={"Authorization": "Bearer mock_token"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["event_id"] == payload["event_id"]
