from datetime import datetime
from typing import List

import pandas as pd
from fastapi import APIRouter, HTTPException, Body
from starlette.responses import JSONResponse

import db_access.pc
from db_access.data import select_total_running_time
from db_access.pc import get_pcs, get_pcs_by_userid, add_pc, get_free_disk_space_data, \
    get_recent_disk_and_partition
from db_access.application import get_latest_application_data
from data_analytics import requests
from exceptions.DataBaseInsertExcepion import DataBaseInsertException
from exceptions.InvalidParametersException import InvalidParametersException
from model.pc import PCItem, ForecastResult, ForecastData, DISKS, Network, PCSpecs, PCMetrics
from model.data import PCData, StatisticData, PCTimeSeriesData

pc = APIRouter()


@pc.get('/', response_model=dict, tags=["PC"])
def get_all_pcs():
    """
    Get all PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs.
    """
    return {'pcs': get_pcs()}


@pc.get('/user/{user_id}', response_model=dict, tags=["PC"])
def get_pc_by_user_id(user_id: str):
    """
    Get PCs by user ID.

    Args:
        user_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
    """
    return {'pcs': get_pcs_by_userid(user_id)}


@pc.post('/add_pc', response_model=dict, status_code=201, tags=["PC"])
def add_pc_api(data: PCItem = Body(...)):
    """
    Add a PC.

    Args:
        data (PCItem): The PC data to add.

    Returns:
        dict: A dictionary with a 'pc_id' key containing the newly inserted PC ID.
    """
    user_id = data.user_id
    hardware_uuid = data.hardware_uuid
    client_name = data.client_name

    pc_id = add_pc(user_id, hardware_uuid, client_name)
    if pc_id == -1:
        raise DataBaseInsertException(code=500, detail="Failed to insert PC.")

    return {'pc_id': pc_id}


@pc.get('/{pc_id}/ram', response_model=PCData, tags=["PC"])
def get_pc_ram(pc_id: int, start: str, end: str, bucket_value: str = '1 minute'):
    """
    Get data from PCs by ID and for a defined type like RAM or CPU

    Args:
        user_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
        :param start:
        :param end:
    """
    ram_df, time_series = db_access.pc.get_ram_time_series_between(pc_id, start, end, bucket_value)

    df, application_data_list = get_latest_application_data(pc_id, 1, None)
    if df is None or ram_df is None:
        raise InvalidParametersException()
    pc_total_df, allocation_list, events_and_anomalies, statistic_data = requests.analyze_pc_data(
        pc_id, df, ram_df, 'ram')

    pc_data = PCData(
        pc_id=pc_id,
        start=start,
        end=end,
        time_series_list=time_series,
        allocation_list=allocation_list,
        events_and_anomalies=events_and_anomalies,
        statistic_data=statistic_data
    )

    print(pc_data)
    return pc_data


@pc.get('/{pc_id}/cpu', response_model=PCData, tags=["PC"])
def get_pc_cpu(pc_id: int, start: str, end: str, bucket_value: str = '1 minutes'):
    """
    Get data from PCs by ID and for a defined type like RAM or CPU

    Args:
        user_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
        :param start:
        :param end:
    """
    cpu_df, time_series = db_access.pc.get_cpu_time_series_between(pc_id, start, end, bucket_value)

    df, application_data_list = get_latest_application_data(pc_id, 1, None)
    if df is None or cpu_df is None:
        raise InvalidParametersException()
    pc_total_df, allocation_list, events_and_anomalies, statistic_data = requests.analyze_pc_data(pc_id,
        df, cpu_df, 'cpu')

    pc_data = PCData(
        pc_id=pc_id,
        start=start,
        end=end,
        time_series_list=time_series,
        allocation_list=allocation_list,
        events_and_anomalies=events_and_anomalies,
        statistic_data=statistic_data
    )

    print(pc_data)
    return pc_data

@pc.get('/{pc_id}/disk', response_model=List[PCTimeSeriesData], tags=["PC"])
def get_pc_disk_space(pc_id: int, start: str, end: str):
    """
    Get data from PCs by ID and for a defined type like RAM or CPU

    Args:
        user_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
        :param start:
        :param end:
    """
    df, disk_space_list = db_access.pc.get_disk_space_between(pc_id, start, end)
    print(df)
    return disk_space_list



@pc.get('/{pc_id}/disks-partitions', response_model=DISKS, tags=["PC"])
def get_pc_disks(pc_id: int):
    """
    Get data from PCs by ID and for a defined type like RAM or CPU

    Args:
        pc_id (int): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
        :param start:
        :param end:
    """
    DISKS = get_recent_disk_and_partition(int(pc_id))

    return DISKS


@pc.get('/{pc_id}/network', response_model=Network, tags=["PC"])
def geet_pc_network(pc_id: int):
    """
    Get data from PCs by ID and for a defined type like RAM or CPU

    Args:
        pc_id (int): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
        :param start:
        :param end:
    """
    connection_list = db_access.pc.select_connections(pc_id)
    network_interface_list = db_access.pc.select_network_interfaces(pc_id)

    network = Network(
        network_list=network_interface_list,
        connection_list=connection_list
    )

    return network


@pc.get('/{pc_id}/data/', response_model=dict, tags=["PC"])
def get_pc_by_user_id(pc_id: int, start: int, end: int):
    """
    Get data from PCs by ID.

    Args:
        user_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
    """
    return {'pc': pc_id, "start": start, "end": end}


@pc.get('/{pc_id}/data/forecast/{days}', response_model=ForecastResult, tags=["PC"])
def forecast_free_disk_space(pc_id: int, days: int):
    """
    Forecasts free disk space data for a certain PC in daily interevals

    Args:
        user_id (str): The pc ID to filter PCs.

    Returns:
        dict: A dictionary with a measurement time and the forecasted free disk space at that time.
        :param days:
    """
    try:
        df = get_free_disk_space_data(pc_id)
        if df is None:
            raise InvalidParametersException()
        data_list, final_timestamp = requests.forecast_disk_space(df, 'free_disk_space', days)
        forecast_result = ForecastResult(
            pc=pc_id,
            days=days,
            final_timestamp=final_timestamp,
            data_list=data_list
        )
        print(forecast_result)
        return forecast_result
    except Exception as e:
        raise InvalidParametersException()


@pc.get('/general_specs/{pc_id}', response_model=PCSpecs, tags=["PC"])
def get_pc_by_user_id(pc_id: str):
    """
    Get specs of PC by user ID.

    Args:
        pc_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
    """

    specs = db_access.pc.general_specs(pc_id)
    return specs


@pc.get('/resource_metrics/{pc_id}', response_model=PCMetrics, tags=["PC"])
def get_pc_by_user_id(pc_id: str):
    """
    Get recource metrics of pc by ID

    Args:
        pc_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
    """

    metrics = db_access.pc.resource_metrics(pc_id)
    return metrics


@pc.get('/{pc_id}/time-metrics/', response_model=dict, tags=["PC"])
def get_pc_time_metrics(pc_id: int, start: datetime, end: datetime):
    time_metrics_dict = select_total_running_time(start, end, pc_id)
    return time_metrics_dict
