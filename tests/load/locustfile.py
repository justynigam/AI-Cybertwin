from locust import HttpUser, task, between
import uuid
from datetime import datetime

class CyberDeviceSimulator(HttpUser):
    # Simulate a device sending a log every 0.1 to 1 second
    wait_time = between(0.1, 1.0)

    @task
    def send_auth_log(self):
        """Simulates a rapid stream of incoming authentication logs."""
        payload = {
            "event_id": str(uuid.uuid4()),
            "user_id": "user_778",
            "device_id": "device_991",
            "event_type": "AUTHENTICATION",
            "timestamp": datetime.utcnow().isoformat(),
            "ip_address": "192.168.1.55"
        }
        
        # POST to the FastAPI ingestion route
        with self.client.post("/api/v1/ingest", json=payload, catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            else:
                response.failure(f"Failed with status: {response.status_code}")
