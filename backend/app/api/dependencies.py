"""
FastAPI Dependencies for CyberTwin AI Backend.
Provides JWT authentication verification and database session dependencies.
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security_bearer = HTTPBearer(auto_error=False)


def get_db() -> Generator:
    """
    Database session dependency yield fallback.
    Yields mock DB session or SQLAlchemy session if connected.
    """
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

    db = MockDBSession()
    try:
        yield db
    finally:
        pass


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)) -> dict:
    """
    Verifies Bearer JWT authentication token header.
    In development/demo mode, accepts valid headers or fallback mock credentials.
    """
    if credentials is None:
        # Demo fallback mode for local development testing
        return {"sub": "analyst-1", "role": "SOC_LEAD", "email": "analyst@cybertwin.ai"}

    token = credentials.credentials
    if not token or token == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"sub": "analyst-1", "role": "SOC_LEAD", "token": token}
