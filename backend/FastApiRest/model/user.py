from datetime import datetime

from pydantic import BaseModel
from typing import List

from model.data import AlertData


class CheckLoginRequest(BaseModel):
    email: str = None
    user_id: str = None
    name: str = None
    password: str


class AddUserRequest(BaseModel):
    name: str
    email: str
    password: str


class UserAlerts(BaseModel):
    user_id: int
    start: datetime
    end: datetime
    alert_list: List[AlertData]
