from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

data = APIRouter()

class ApplicationData(BaseModel):
    measurement_time: str
    name: str
    path: str
    cpu: float
    ram: int
    State: str
    user: str
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
    applicationdata_anomaly: Dict[str, int]  # Update: Add this field for applicationdata_anomaly

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

@data.post("/", description="Insert Timeseries data", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def injest_all_data(data: TimeseriesData):
    """
    Insert Timeseries data.

    Args:
        data (TimeseriesData): The Timeseries data to insert.

    Returns:
        dict: A dictionary with a 'result' key indicating the success or failure of the operation.
    """
    try:
        pcdata = data.pcdata
        applicationdata = data.applicationdata
        applicationdata_anomaly = data.applicationdata_anomaly
        networkInterface = data.networkInterface

        # Do something with the data...

        return {"result": "Data inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
