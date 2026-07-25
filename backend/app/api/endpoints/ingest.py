"""
FastAPI Event Ingestion Endpoint for CyberTwin AI Backend.
POST /ingest receives raw audit/authentication telemetry logs for real-time ML processing
and WebSocket alert broadcast.
"""
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.event_schemas import TelemetryEventIngest, IngestResponse
from backend.app.api.dependencies import verify_token
from backend.app.workers.inference_worker import MLInferenceWorker
from backend.app.api.endpoints.websockets import manager

router = APIRouter()
inference_worker = MLInferenceWorker()


@router.post("/", response_model=IngestResponse, summary="Ingest real-time security event")
async def ingest_event(
    event: TelemetryEventIngest,
    current_user: dict = Depends(verify_token)
):
    """
    Ingests a raw telemetry log event into CyberTwin AI real-time stream
    and broadcasts calculated anomaly alerts over WebSocket.
    """
    try:
        event_dict = event.model_dump()
        event_dict["timestamp"] = event.timestamp.isoformat()

        success, alert_payload = inference_worker.process_event(event_dict)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to process event through ML pipeline")

        # Broadcast the generated alert dynamically over WebSockets to all React clients
        if alert_payload:
            asyncio.create_task(manager.broadcast(alert_payload))

        return IngestResponse(
            status="success",
            event_id=event.event_id,
            message="Event successfully ingested into CyberTwin AI pipeline"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
