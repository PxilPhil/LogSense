from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel


class CustomCondition(BaseModel):
    percentage_trigger_value: Optional[float] = None
    degree_trigger_value: Optional[int] = None
    absolute_trigger_value: Optional[int] = None
    operator: Optional[str] = None
    column: Optional[str] = None
    application: Optional[str] = None
    lookback_time: Optional[int] = None
    start_date: Optional[str] = None
    order: Optional[int] = None
    logical_condition: Optional[str] = None
    conditions: Optional[List[CustomCondition]] = None  # maybe replace with CustomCondition


class CustomAlert(BaseModel):
    user_id: int
    type: str
    message: str
    severity_level: int
    conditions: List[CustomCondition]


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