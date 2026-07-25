"""
Global PyTest fixtures for CyberTwin AI testing suite.
Provides TestClient, mock database sessions, and synthetic telemetry fixtures.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.app.main import app


@pytest.fixture(scope="module")
def test_client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db_session():
    """Mock database session fixture."""
    class MockDBSession:
        def query(self, model):
            return self
        def filter(self, *args, **kwargs):
            return self
        def order_by(self, *args, **kwargs):
            return self
        def offset(self, skip):
            return self
        def limit(self, limit):
            return self
        def all(self):
            return []
        def first(self):
            return None

    return MockDBSession()
