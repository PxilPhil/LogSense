from __future__ import annotations
from pydantic import BaseModel, Json
from typing import List
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from model.pc import Connection, NetworkInterface, Disk


# TODO: Keep in mind to return AlertData to user instead of respective classes used for saving data


class EventData(BaseModel):  # TODO: deprecated but kept in application to avoid db errors
    timestamp: datetime
    anomaly_type: int
    change: float
    application: str
    column: str


class Justification(BaseModel):  # class containing justification data
    timestamp: datetime
    till_timestamp: datetime
    is_anomaly: bool
    justification_message: str


class AnomalyData(BaseModel):  # anomaly data class returned when analyzing application data
    timestamp: datetime
    severity: int  # calculated via z-score
    column: str
    justification: Optional[Justification]


class AlertData(BaseModel):  # basically AnomalyData (EventData) but includes custom alerts and are returned to the user
    type: str
    severity_level: int  # TODO: Either map in frontend or change severity_level to a string
    message: str
    change_in_percentage: float
    name: str
    measurement_time: datetime
    pc_id: int


class PCTimeSeriesData(BaseModel):
    measurement_time: datetime
    ram: float
    cpu: float
    # method to parse a dictionary and create a PCTimeSeriesData object
    @classmethod
    def from_dict(cls, data):
        # Convert the 'measurement_time' from string to a datetime object
        data['measurement_time'] = datetime.strptime(data['measurement_time'], "%Y-%m-%d %H:%M:%S.%f")
        return cls(**data)


class AllocationClass(BaseModel):
    name: str
    allocation: float


class StatisticData(BaseModel):
    latest_ram: float
    latest_cpu: float
    oldest_ram: float
    oldest_cpu: float
    average_ram: float
    median_ram: float
    average_cpu: float
    median_cpu: float
    stability: str
    message: str


class PCData(BaseModel):
    pc_id: int
    start: str
    end: str
    time_series_list: List[PCTimeSeriesData]
    allocation_list_ram: List[AllocationClass]
    allocation_list_cpu: List[AllocationClass]
    ram_events_and_anomalies: List[Justification]
    cpu_events_and_anomalies: List[Justification]
    statistic_data: StatisticData
