from __future__ import annotations
from pydantic import BaseModel, Json
from typing import List
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from model.data import EventData, AnomalyData, Justification, StatisticData


class ApplicationTimeSeriesData(BaseModel):
    id: int
    pcdata_id: int
    measurement_time: datetime
    name: str
    path: str
    cpu: float
    ram: int
    state: str
    user: str
    context_switches: int
    major_faults: int
    bitness: int
    commandline: str
    current_Working_Directory: str
    open_files: int
    parent_process_id: int
    thread_count: int
    uptime: int
    process_count_difference: int
    moving_average_ram: float
    moving_average_cpu: float


class ApplicationData(BaseModel):
    pc: int
    application_name: str
    time_series_data: List[ApplicationTimeSeriesData]
    cpu_events_and_anomalies: List[Justification]
    ram_events_and_anomalies: List[Justification]
    statistic_data: StatisticData


class ApplicationListObject(BaseModel):
    pc_id: int
    start: datetime
    end: datetime
    application_list: List[str]
