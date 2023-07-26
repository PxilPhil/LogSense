from typing import List

import pandas as pd

from data_analytics import requests
from fastapi import HTTPException, APIRouter, UploadFile
from fastapi.responses import JSONResponse
from model.data import runningPCData, sessionPCData

from db_access.data import insert_pcdata

data = APIRouter()


@data.post("/initial", description="Insert Timeseries data", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def injest_initial_data(data: sessionPCData):
    """
    Insert Initial data.

    Args:
        data (sessionPCData): The data which only change once per session

    Returns:
    - dict: Response message confirming successful data submission.
    """
    try:
        pcdata = data.pcdata

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": 1}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")


@data.post("/", description="Insert Timeseries data", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def ingest_data(files: list[UploadFile]):

    """
    Insert Timeseries data.

    Args:
        data (runningPCData): The Timeseries data to insert each of the datapoints

    Returns:
        dict: A dictionary with a 'result' key indicating the success or failure of the operation and 'pcdata_id' the ID of the pcData inserted
    """
    try:
        df_map = dict()
        print(files)
        for file in files:
            df_map[file.filename] = pd.read_csv(file.file, sep='|')
        print(df_map)


        pcdata = df_map["resources"]
        application_data = df_map["application"]

        print(application_data)
        pc_total_df, anomaly_map = requests.ingest_process_data(df_map["application"])

        # TODO: Insert multiple dataframes, so far we only do it for application dataframes
        pcdata_id = insert_pcdata(df_map, pc_total_df, anomaly_map)

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": 0}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
