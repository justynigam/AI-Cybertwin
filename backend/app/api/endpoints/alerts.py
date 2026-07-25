from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime

from backend.app.api.dependencies import get_db, verify_token
from backend.app.schemas.alert_schemas import AlertResponse

router = APIRouter()

# In-memory store fallback for demo alerts if database is unpopulated
MOCK_ALERTS = [
    {
        "id": "c1be6ce7-c1c9-4075-98a4-ebffebec2843",
        "timestamp": datetime.utcnow().isoformat(),
        "severity": "CRITICAL",
        "attack_category": "Impossible Travel",
        "master_risk_score": 0.98,
        "nlp_explanation": "This event was flagged due to impossible travel speed between geographical locations combined with accessing a sensitive resource for the first time.",
        "user_id": "usr-9982",
        "device_id": "dev-4410",
        "ip_address": "185.220.101.4",
        "twin_predictions": [
            {"predicted_action": "Access_HR_Database", "probability_score": 0.82, "rank": 1}
        ]
    },
    {
        "id": "e89b2104-5512-4011-9122-119201928301",
        "timestamp": datetime.utcnow().isoformat(),
        "severity": "HIGH",
        "attack_category": "Lateral Movement",
        "master_risk_score": 0.84,
        "nlp_explanation": "This event was flagged due to sudden network hop distance increase across 3 isolated subnets.",
        "user_id": "usr-3104",
        "device_id": "dev-8812",
        "ip_address": "10.0.4.99",
        "twin_predictions": [
            {"predicted_action": "Privilege_Escalation_Attempt", "probability_score": 0.74, "rank": 1}
        ]
    }
]


@router.get("/", response_model=List[AlertResponse], summary="List all security alerts")
def get_alerts(
    skip: int = Query(0, ge=0, description="Pagination skip"),
    limit: int = Query(100, ge=1, le=1000, description="Pagination limit"),
    severity: str = Query(None, description="Filter by severity (e.g., CRITICAL)"),
    db: any = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """
    Retrieve historical security alerts.
    - Requires a valid JWT token.
    - Supports pagination and severity filtering.
    """
    alerts = MOCK_ALERTS

    if severity:
        alerts = [a for a in alerts if a["severity"] == severity.upper()]

    paginated_alerts = alerts[skip : skip + limit]

    if not paginated_alerts and skip == 0:
        raise HTTPException(status_code=404, detail="No alerts found.")

    return paginated_alerts


@router.get("/{alert_id}", response_model=AlertResponse, summary="Get a specific alert")
def get_alert_by_id(
    alert_id: str,
    db: any = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    alert = next((a for a in MOCK_ALERTS if a["id"] == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found.")
    return alert
