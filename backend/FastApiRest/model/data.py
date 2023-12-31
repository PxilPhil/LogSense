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

class JustificationData(BaseModel):  # class containing explanation, justification and details about an event or anomaly
    application: str
    started: bool
    stopped: bool
    process_change: int
    delta_ram: float
    delta_cpu: float
    warning: bool


class EventAnomalyJustifications(BaseModel):  # class containing justifications for events and anomalies
    timestamp: datetime
    justification_list: List[JustificationData]


class AnomalyData(BaseModel):  # anomaly data class returned when analyzing application data
    timestamp: datetime
    severity: int  # calculated via z-score
    column: str
    justification: Optional[EventAnomalyJustifications]


class AlertData(BaseModel):  # basically AnomalyData (EventData) but includes custom alerts and are returned to the user
    type: str
    severity_level: int  # TODO: Either map in frontend or change severity_level to a string
    message: str
    change_in_percentage: float
    name: str
    measurement_time: datetime
    pc_id: int


class PCTimeSeriesData(BaseModel):
    id: int
    state_id: int
    pc_id: int
    measurement_time: datetime
    free_disk_space: float
    read_bytes_disks: float
    reads_disks: int
    write_bytes_disks: float
    writes_disks: int
    partition_major_faults: int
    partition_minor_faults: int
    available_memory: float
    names_power_source: str
    charging_power_sources: bool
    discharging_power_sources: bool
    power_online_power_sources: bool
    remaining_capacity_percent_power_sources: float
    context_switches_processor: int
    interrupts_processor: int
    ram: float
    cpu: float
    context_switches: int
    major_faults: int
    open_files: int
    thread_count: int

    # method to parse a dictionary and create a PCTimeSeriesData object
    @classmethod
    def from_dict(cls, data):
        # Convert the 'measurement_time' from string to a datetime object
        data['measurement_time'] = datetime.strptime(data['measurement_time'], "%Y-%m-%d %H:%M:%S.%f")
        return cls(**data)


class AllocationClass(BaseModel):
    name: str
    allocation: float


class PCData(BaseModel):
    pc_id: int
    start: str
    end: str
    standard_deviation_ram: float
    mean_ram: float
    standard_deviation_cpu: float
    mean_cpu: float
    time_series_list: List[PCTimeSeriesData]
    allocation_list_ram: List[AllocationClass]
    allocation_list_cpu: List[AllocationClass]
    ram_events: List[EventAnomalyJustifications]
    cpu_events: List[EventAnomalyJustifications]
    ram_anomalies: List[EventAnomalyJustifications]
    cpu_anomalies: List[EventAnomalyJustifications]
