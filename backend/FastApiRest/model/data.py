from pydantic import BaseModel, Json
from typing import List
from datetime import datetime

# TODO: Keep in mind to return AlertData to user instead of respective classes used for saving data

class sessionPCData(BaseModel):
    disks: str
    partition: str
    client_data: str


class runningPCData(BaseModel):
    pc_resources: str
    connection_data: str
    application_data: str
    network_Interface: str


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


class ApplicationListObject(BaseModel):
    pc_id: int
    start: datetime
    end: datetime
    application_list: List[str]


class EventData(BaseModel):  # anomaly data class returned when analyzing application data
    timestamp: datetime
    anomaly_type: int
    change: float
    application: str
    column: str


class AnomalyData(BaseModel):  # anomaly data class returned when analyzing application data
    timestamp: datetime
    severity: int  # calculated via z-score
    application: str
    column: str


class AlertData(BaseModel):  # basically AnomalyData (EventData) but includes custom alerts and are returned to the user
    type: str
    severity_level: int  #TODO: Either map in frontend or change severity_level to a string
    message: str
    change_in_percentage: float
    data_type: str
    name: str
    measurement_time: datetime
    pc_id: int


class ApplicationData(BaseModel):
    pc: int
    application_name: str
    standard_deviation: float
    mean: float
    time_series_data: List[ApplicationTimeSeriesData]
    event_list: List[EventData]
    anomaly_list: List[AnomalyData]


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


class PCData(BaseModel):  # Missing Trends
    pc_id: int
    type: str
    start: str
    end: str
    standard_deviation: float
    mean: float
    time_series_list: List[PCTimeSeriesData]
    allocation_map: List[AllocationClass]
    anomaly_list: List[AnomalyData]
