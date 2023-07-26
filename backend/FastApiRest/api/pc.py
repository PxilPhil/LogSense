import pandas as pd
from fastapi import APIRouter, HTTPException, Body
from db_access.pc import get_pcs, get_pcs_by_userid, add_pc
from data_analytics import requests
from model.pc import PCItem


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
        raise HTTPException(status_code=500, detail="Failed to insert PC.")

    return {'pc_id': pc_id}


@pc.get('/{pc_id}/data/{type}', response_model=dict, tags=["PC"])
def get_pc_by_user_id(pc_id: int,type: str, start: int, end: int):
    """
    Get data from PCs by ID and from Type type.

    Args:
        user_id (str): The user ID to filter PCs.

    Returns:
        dict: A dictionary with a 'pcs' key containing a list of PCs filtered by user ID.
    """
    try:
        column = ''
        if type == 'RAM':
            column = 'residentSetSize'
        elif type == 'CPU':
            column = 'cpuUsage'
        else:
            raise HTTPException(status_code=400, detail="Not implemented yet")

        pc_total_df, allocation_map, std, mean, trend_list, involvement_map = requests.fetch_pc_data(pd.DataFrame(), column)
        print(pc_total_df, allocation_map, std, mean, trend_list, involvement_map)
        return {'pc': pc_id, 'type': type, "start": start, "end": end}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

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
