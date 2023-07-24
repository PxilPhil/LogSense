from data_analytics import requests
from fastapi import HTTPException, APIRouter
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

        pcdata_id = insert_pcdata(pcdata)

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": pcdata_id}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")


@data.post("/", description="Insert Timeseries data", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def injest_data(data: runningPCData):
    """
    Insert Timeseries data.

    Args:
        data (runningPCData): The Timeseries data to insert each of the datapoints

    Returns:
        dict: A dictionary with a 'result' key indicating the success or failure of the operation and 'pcdata_id' the ID of the pcData inserted
    """
    return 0 #TODO: implement
    try:
        pcdata = data.pcdata
        application_data = data.application_data

        # TODO: GET CSV AND INSERT IT HERE
        anomaly_map = requests.ingest_process_data(application_data)

        # TODO: Remove later on
        for key, obj_list in anomaly_map.items():
            print("Key:", key)
            for obj in obj_list:
                print("Object timestamp:", obj.timestamp)
                print("Object anomalyType:", obj.isEvent)
        pcdata_id = insert_pcdata(pcdata)

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": pcdata_id}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

@data.get("/", description="Fetch Timeseries data", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def fetch_data(pc_id):
    """
    Fetch Timeseries data from PC

    Args:
        data (TimeseriesData): The Timeseries data to fetch.

    Returns:
        dict: A dictionary with a 'result' key indicating the success or failure of the operation.
    """
    try:
        # TODO: GET CSV AND INSERT IT HERE
        trends = requests.fetch_process_trends()

        #TODO: Remove later
        for entry in trends:
            print(entry.change)
        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": 0}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

@data.get("/application", description="Fetch Timeseries data for a certain Application", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def fetch_app_data(name):
    """
    Fetch Timeseries data from PC

    Args:
        data (TimeseriesData): The Timeseries data to fetch.

    Returns:
        dict: A dictionary with a 'result' key indicating the success or failure of the operation.
    """
    try:
        # TODO: GET CSV AND INSERT IT HERE
        anomaly_list = requests.fetch_application_data(name)

        #TODO: Remove later
        for entry in anomaly_list:
            print(entry.is_event)

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": 0}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
