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


class PCState(BaseModel):
    id: int
    measurement_time: str
    pc_id: int
    total_memory_size: int
    memory_page_size: int
    processor_name: str
    processor_identifier: str
    processor_id: str
    processor_vendor: str
    processor_bitness: int
    physical_package_count: int
    physical_processor_count: int
    logical_processor_count: int


class ForecastData(BaseModel):
    LinearRegression: float
    datetime: datetime


class ForecastResult(BaseModel):
    pc: int
    days: int
    final_timestamp: Optional[datetime]
    data_list: List[ForecastData]


class sessionPCData(BaseModel):
    disks: str
    partition: str
    client_data: str


class runningPCData(BaseModel):
    pc_resources: str
    connection_data: str
    application_data: str
    network_Interface: str


class PARTITION(BaseModel):
    id: int
    disk_id: int
    disk_store_name: str
    identification: str
    name: str
    type: str
    mount_point: str
    size: int
    major_faults: int
    minor_faults: int


class DISK(BaseModel):
    id: int
    state_id: int
    measurement_time: datetime
    serialnumber: str
    model: str
    name: str
    size: int
    partitions: List[PARTITION]


class DISKS(BaseModel):
    disks: List[DISK]


class NetworkInterface(BaseModel):
    id: int
    pcdata_id: int
    name: str
    display_name: str
    ipv4_address: str
    ipv6_address: str
    subnet_mask: str
    mac_address: str
    bytes_received: int
    bytes_sent: int
    packets_received: int
    packets_sent: int


class Connection(BaseModel):
    id: int
    pcdata_id: int
    localaddress: str
    localport: int
    foreignaddress: str
    foreignport: int
    state: str
    type: str
    owningprocessid: int


class Network(BaseModel):
    network_list: List[NetworkInterface]
    connection_list: List[Connection]


class DiskPartition(BaseModel):
    id: int
    disk_id: int
    disk_store_name: str
    identification: str
    name: str
    type: str
    mount_point: str
    size: int
    major_faults: int
    minor_faults: int


class Disk(BaseModel):
    id: int
    state_id: int
    measurement_time: datetime
    serialnumber: str
    model: str
    name: str
    size: int
    disk_partition_list: List[DiskPartition] = []


class PCDetails(BaseModel):
    runtime_in_seconds: float
    manufacturer: Optional[str]
    model: Optional[str]
    hardware_uuid: str
    system_battery: str
    remaining_capacity: float
    charging: bool
    discharging: bool
    power_on_line: bool

class PCSpecs(BaseModel):
    processor_name: str
    processor_identifier: str
    processor_id: str
    processor_vendor: str
    processor_bitness: int
    physical_package_count: int
    physical_processor_count: int
    logical_processor_count: int
    context_switches: int
    interrupts: int

class PCMetrics(BaseModel):
    avg_cpu_usage_percentage_last_day: float
    cpu_percentage_use: float
    cpu_stability: str
    processor_name: str
    physical_package_count: int
    physical_processor_count: int
    logical_processor_count: int
    avg_ram_usage_percentage_last_day: float
    ram_percentage_in_use: float
    ram_stability: str
    total_memory: int
    free_memory: int
    page_size: int
    disk_percentage_in_use: float
    total_disk_space: int
    free_disk_space: int
