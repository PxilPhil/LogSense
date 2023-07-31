from pydantic import BaseModel
from typing import List
from datetime import datetime


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


class ApplicationListObject(BaseModel):
    pc_id: int
    start: datetime
    end: datetime
    application_list: List[str]


class AnomalyData(BaseModel):
    anomaly_type: int
    timestamp: int
    change: float
    application: str
    column: str


class ApplicationData(BaseModel):
    pc: int
    application_name: str
    standard_deviation: float
    mean: float
    time_series_data: List[ApplicationTimeSeriesData]
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


"""
class NetworkInterface(BaseModel):
    name: str
    display_name: str
    ipv4_address: str
    ipv6_address: str
    art: str
    subnet_mask: str
    mac_address: str
    bytes_received: int
    bytes_sent: int
    packets_received: int
    packets_sent: int

class PCData(BaseModel):
    session_id: int
    measurement_time: str
    free_disk_space: int
    partition_major_faults: int
    partition_minor_faults: int
    available_memory: int
    names_power_source: str
    discharging_power_sources: bool
    power_online_power_sources: bool
    remaining_capacity_percent_power_sources: float
    context_switches_processor: int
    interrupts_processor: int
    applicationdata: List[ApplicationData]
    networkInterface: List[NetworkInterface]

class TimeseriesData(BaseModel):
    pcdata: PCData
"""
