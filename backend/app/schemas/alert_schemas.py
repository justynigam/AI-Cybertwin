from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class AlertBase(BaseModel):
    severity: str = Field(..., pattern="^(CRITICAL|HIGH|MEDIUM|LOW)$")
    attack_category: str
    master_risk_score: float = Field(..., ge=0.0, le=1.0)
    nlp_explanation: Optional[str] = None

class AlertResponse(AlertBase):
    id: str
    timestamp: datetime
    user_id: Optional[str] = None
    device_id: Optional[str] = None
    ip_address: Optional[str] = None
    twin_predictions: List[Dict] = []
    
    class Config:
        from_attributes = True # Allows Pydantic to read from ORM models
