import pandas as pd
from fastapi import APIRouter, HTTPException, Body

import db_access.pc
from db_access.pc import get_pcs, get_pcs_by_userid, add_pc, get_pc_data, get_free_disk_space_data
from db_access.application import get_latest_application_data
from data_analytics import requests
from exceptions.DataBaseInsertExcepion import DataBaseInsertException
from exceptions.InvalidParametersException import InvalidParametersException
from model.pc import PCItem, ForecastResult, ForecastData
from model.data import PCData

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


@pc.get('/{pc_id}/data', response_model=PCData, tags=["PC"])
def get_pc_data(pc_id: int, start: str, end: str):
    """
    Get data from PCs by ID and for a defined type like RAM or CPU

    Args:
        user_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
        :param start:
        :param end:
    """
    total_df, total_data_list = db_access.pc.get_total_pc_application_data(pc_id, start, end)
    connection_list = db_access.pc.select_connections(pc_id)
    network_list = db_access.pc.select_network_interfaces(pc_id)
    disk_list = db_access.pc.select_disks(pc_id)

    df, application_data_list = get_latest_application_data(pc_id)
    if df is None or total_df is None:
        raise InvalidParametersException()
    pc_total_df, anomaly_list, allocation_list_ram, allocation_list_cpu, std_ram, mean_ram, std_cpu, mean_cpu = requests.analyze_pc_data(df, total_df)

        # TODO: Analyzing cpu data doesnt really makesense(atleast like RAM), remove feature or take a closer look at it

    pc_data = PCData(
        pc_id=pc_id,
        start=start,
        end=end,
        standard_deviation_ram=std_ram,
        mean_ram=mean_ram,
        standard_deviation_cpu=std_cpu,
        mean_cpu=mean_cpu,
        time_series_list=total_data_list,
        allocation_list_ram=allocation_list_ram,
        allocation_list_cpu=allocation_list_cpu,
        anomaly_list=anomaly_list
    )

    print(pc_data)
    return pc_data



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
        data_list, final_timestamp = requests.forecast_disk_space(df, days)
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

