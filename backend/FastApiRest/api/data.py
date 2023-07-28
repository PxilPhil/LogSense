from typing import List

import pandas as pd

from data_analytics import requests
from fastapi import HTTPException, APIRouter, UploadFile
from fastapi.responses import JSONResponse

from db_access.data_helper import get_dfdict_from_filelist, get_pc_state_df
from model.data import runningPCData, sessionPCData

from db_access.data import insert_running_pcdata, get_moving_avg_of_total_ram, insert_inital_pcdata

data = APIRouter()


@data.post("/initial", description="Check PC State", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def injest_initial_data(files: list[UploadFile]):
    """
    Insert Initial data.

    Args:
        files (list[UploadFile]): A list of UploadFile objects representing the Timeseries data files.
            - File names must include: "client", "disk", "partition"

    Returns:
        dict:
        A dictionary with a 'result' key indicating the success or failure of the operation,
        'pcdata_id' the ID of the pcData inserted,
        and 'Anomalies found' indicating the number of anomalies detected.
    """
    state_id = None
    try:
        df_dict = get_dfdict_from_filelist(files)

        state_id = insert_inital_pcdata(df_dict)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

    if not state_id:
        raise HTTPException(status_code=400, detail="Pc does Not Exsist")

    return JSONResponse(content={"result": "Data inserted successfully", "state_id": state_id}, status_code=200)



@data.post("/", description="Insert Timeseries data", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def ingest_data(files: list[UploadFile], stateId: int):
    """
    Insert Timeseries data.

    Args:
        stateId (int): The ID of the state.
        files (list[UploadFile]): A list of UploadFile objects representing the Timeseries data files.
            - File names must include: "application", "connection", "resources", "network".

    Returns:
        dict:
        A dictionary with a 'result' key indicating the success or failure of the operation,
        'pcdata_id' the ID of the pcData inserted,
        and 'Anomalies found' indicating the number of anomalies detected.
    """
    try:
        df_map = get_dfdict_from_filelist(files)

        pcdata = df_map["resources"]
        application_data = df_map["application"]

        print(application_data)
        pc_total_df, anomaly_map = requests.ingest_process_data(df_map["application"])

        # TODO: Insert multiple dataframes, so far we only do it for application dataframes
        pcdata_id = insert_running_pcdata(stateId, df_map, pc_total_df, anomaly_map)

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": pcdata_id, "Anomalies found:": len(anomaly_map)}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
