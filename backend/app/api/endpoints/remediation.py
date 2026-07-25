"""
FastAPI Remediation endpoints for CyberTwin AI Backend.
Exposes REST endpoints to generate security advisor playbooks and trigger automated remediation actions.
"""
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from backend.app.services.security_advisor import SecurityAdvisorPlaybook

router = APIRouter(prefix="/remediation", tags=["remediation"])
advisor = SecurityAdvisorPlaybook()


class AlertContextRequest(BaseModel):
    severity: str = Field(default="HIGH", description="Alert severity: CRITICAL, HIGH, MEDIUM, LOW")
    attack_category: str = Field(default="Impossible Travel", description="MITRE ATT&CK or anomaly category")
    twin_predictions: list[dict] = Field(default_factory=list, description="Top predicted next steps from Behavioral Twin")


class ActionExecutionRequest(BaseModel):
    action_id: str = Field(..., description="Action ID to execute (e.g., FORCE_MFA, ISOLATE_HOST, BLOCK_IP)")
    target_entity: str = Field(..., description="Target entity ID, IP, user_id, or device_id")


@router.post("/recommendations")
def get_recommendations(context: AlertContextRequest):
    """
    Returns actionable remediation playbooks and automated defense steps for an alert context.
    """
    try:
        recommendations = advisor.generate_recommendations(context.model_dump())
        return {
            "status": "success",
            "context": context.model_dump(),
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
def execute_remediation_action(request: ActionExecutionRequest):
    """
    Triggers/executes a remediation playbook action against a target user/device/IP.
    """
    try:
        result = advisor.execute_action(action_id=request.action_id, target_entity=request.target_entity)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
