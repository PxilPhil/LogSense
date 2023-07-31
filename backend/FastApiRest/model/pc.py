from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Optional



class PCItem(BaseModel):
    user_id: str
    hardware_uuid: str
    client_name: str
    manufacturer: str = None
    model: str = None


class ForecastData(BaseModel):
    LinearRegression: float
    datetime: datetime


class ForecastResult(BaseModel):
    pc: int
    days: int
    final_timestamp: Optional[datetime]
    data_list: List[ForecastData]
