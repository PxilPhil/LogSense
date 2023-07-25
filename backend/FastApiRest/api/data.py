from typing import List

from data_analytics import requests
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File
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

        pcdata_id = insert_pcdata(pcdata)

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": pcdata_id}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")


@data.post("/", description="Insert Timeseries data", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def ingest_data_(files: List[UploadFile]):
    """
    Insert Timeseries data.

    Args:
        data (runningPCData): The Timeseries data to insert each of the datapoints

    Returns:
        dict: A dictionary with a 'result' key indicating the success or failure of the operation and 'pcdata_id' the ID of the pcData inserted
    """
    try:
        print(files)
        for entry in files:
            print(entry)
        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": 0}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
