from pydantic import BaseModel
from typing import List


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
    measurement_time: str
    name: str
    path: str
    cpu: float
    ram: int
    state: str
    context_Switches: int
    major_Faults: int
    bitness: int
    commandline: str
    current_Working_Directory: str
    open_Files: int
    parent_ProcessID: int
    thread_Count: int
    uptime: int
    process_Count_Difference: int
    # applicationdata_anomaly: int #TODO: check if needed in definition (should be done here, right)


class PCData(BaseModel):
    pc_id: int
    type: str
    start: str
    end: str
    standard_deviation: float
    mean: float


class Anomaly(BaseModel):
    timestamp: str
    change: float
    application: str
    type: str
    pc_id: int


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
