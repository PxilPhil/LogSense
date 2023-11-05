from __future__ import annotations
from pydantic import BaseModel, Json
from typing import List
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from model.data import Justification, StatisticData


class ApplicationTimeSeriesData(BaseModel):
    measurement_time: datetime
    cpu: float
    ram: float


class TimeMetricData(BaseModel):
    name: str
    total_running_time_seconds: float


class TimeMetricDataList(BaseModel):
    data: List[TimeMetricData]


class ApplicationInfo(BaseModel):
    process_id: int
    path: str
    working_directory: str
    command_line: str
    windows_user_name: str
    bitness: int
    state: str
    major_faults: int
    context_switches: int
    threads: int
    open_files: int


class ApplicationListObject(BaseModel):
    pc_id: int
    start: datetime
    end: datetime
    application_list: List[str]


class ApplicationData(BaseModel):
    pc: int
    application_name: str
    time_series_data: List[ApplicationTimeSeriesData]
    cpu_events_and_anomalies: List[Justification]
    ram_events_and_anomalies: List[Justification]
    cpu_statistic_data: StatisticData
    ram_statistic_data: StatisticData
    run_time_in_seconds: TimeMetricData
    info: ApplicationInfo