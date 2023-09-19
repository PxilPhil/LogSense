from __future__ import annotations
from pydantic import BaseModel, Json
from typing import List
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from model.data import EventData, AnomalyData, EventAnomalyJustifications


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
    rolling_avg_ram: float
    rolling_avg_cpu: float


class ApplicationData(BaseModel):
    pc: int
    application_name: str
    standard_deviation_ram: float
    standard_deviation_cpu: float
    mean_ram: float
    mean_cpu: float
    time_series_data: List[ApplicationTimeSeriesData]
    cpu_events: List[EventAnomalyJustifications]
    ram_events: List[EventAnomalyJustifications]
    cpu_anomalies: List[datetime]
    ram_anomalies: List[datetime]


class ApplicationListObject(BaseModel):
    pc_id: int
    start: datetime
    end: datetime
    application_list: List[str]
