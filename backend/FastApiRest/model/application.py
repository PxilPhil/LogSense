from __future__ import annotations
from pydantic import BaseModel, Json
from typing import List
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from model.data import EventData, AnomalyData, Justification, StatisticData


class ApplicationTimeSeriesData(BaseModel):
    measurement_time: datetime
    cpu: float
    ram: int


class ApplicationData(BaseModel):
    pc: int
    application_name: str
    time_series_data: List[ApplicationTimeSeriesData]
    cpu_events_and_anomalies: List[Justification]
    ram_events_and_anomalies: List[Justification]
    cpu_statistic_data: StatisticData
    ram_statistic_data: StatisticData


class ApplicationListObject(BaseModel):
    pc_id: int
    start: datetime
    end: datetime
    application_list: List[str]
