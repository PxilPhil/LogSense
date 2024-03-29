from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from model.data import Justification


class CustomCondition(BaseModel):
    percentage_trigger_value: Optional[float] | str = None # has to be str for json
    absolute_trigger_value: Optional[float] | str = None # has to be str for json
    operator: str
    column: str
    application: Optional[str] = None
    detect_via_moving_averages: bool


class CustomAlert(BaseModel):
    id: int
    user_id: int
    type: str
    message: str
    severity_level: int
    conditions: List[CustomCondition] = []


class CustomAlerts(BaseModel):
    custom_alert_list: List[CustomAlert] = []

    def to_dict(self):
        return self.dict()


class CustomAlertDBObject(BaseModel):
    user_id: int
    type: str
    message: str
    severity_level: int
    conditions: str


class IngestCustomAlert(BaseModel):
    custom_alert_list: List[CustomAlertDBObject]


class AlertNotification(BaseModel):  # the actual alert returned to the user
    type: str
    message: str
    severity_level: int
    column: str
    application: Optional[str]
    detected_alert_list: List[datetime]
