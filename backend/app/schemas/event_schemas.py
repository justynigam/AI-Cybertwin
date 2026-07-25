from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TelemetryEventIngest(BaseModel):
    event_id: str = Field(..., description="Unique UUID event identifier")
    user_id: str = Field(..., description="User ID entity")
    device_id: str = Field(..., description="Primary device identifier")
    event_type: str = Field(default="AUTHENTICATION", description="Event category")
    action: str = Field(default="LOGIN_SUCCESS", description="Action code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    ip_address: str = Field(..., description="Source IP address")
    geo_location: Optional[str] = Field(None, description="City / geo-location string")
    is_attack: bool = Field(default=False, description="Synthetic ground truth attack flag")
    attack_category: Optional[str] = Field(default="None", description="Attack category name")


class IngestResponse(BaseModel):
    status: str
    event_id: str
    message: str
