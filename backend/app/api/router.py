"""
Central API Router for CyberTwin AI Backend.
Combines alerts, ingest, entities, remediation, and websocket stream endpoints.
"""
from fastapi import APIRouter
from backend.app.api.endpoints.alerts import router as alerts_router
from backend.app.api.endpoints.ingest import router as ingest_router
from backend.app.api.endpoints.entities import router as entities_router
from backend.app.api.endpoints.remediation import router as remediation_router
from backend.app.api.endpoints.websockets import router as websockets_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
api_router.include_router(ingest_router, prefix="/ingest", tags=["ingest"])
api_router.include_router(entities_router, prefix="/entities", tags=["entities"])
api_router.include_router(remediation_router, tags=["remediation"])
api_router.include_router(websockets_router, tags=["websockets"])
