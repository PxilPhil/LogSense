from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel


class CustomCondition(BaseModel):
    combined_conditions: Optional[CustomCondition] = None
    percentage_trigger_value: Optional[float] = None
    absolute_trigger_value: Optional[int] = None
    operator: str
    column: str
    application: Optional[str] = None

class CustomAlert(BaseModel):
    user_id: int
    type: str
    message: str
    severity_level: int
    conditions: List[CustomCondition]  # Use List instead of list

class CustomAlerts(BaseModel):
    custom_alert_list: List[CustomAlert]


class CustomAlertDBObject(BaseModel):
    user_id: int
    type: str
    message: str
    severity_level: int
    conditions: str

class IngestCustomAlert(BaseModel):
    custom_alert_list: List[CustomAlertDBObject]