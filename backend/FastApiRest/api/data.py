from fastapi import UploadFile
from fastapi.responses import JSONResponse

from fastapi import APIRouter, HTTPException
from data_analytics import requests


from db_access.data_helper import get_dfdict_from_filelist
from db_access.data import insert_running_pcdata, insert_inital_pcdata
from exceptions.InvalidParametersException import InvalidParametersException
from exceptions.NotFoundExcepion import NotFoundException

data = APIRouter()


@data.post("/initial", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def ingest_initial_data(files: list[UploadFile]):
    """
    **Insert Initial data.**

        Inserts initial data into the system using a list of data files. (Content-Type: multipart/form-data)

    **Parameters:**

    - **files** (list[UploadFile]): A list of UploadFile objects representing the Timeseries data files.

        File names must include: "client", "disk", "partition"

    **Returns:**

    - **dict**: A dictionary with the following keys:
        - 'result': A string indicating the success or failure of the operation.
        - 'state_id': The ID of the pcData inserted.
        - 'Anomalies found': The number of anomalies detected.

    """
    state_id = None
    try:
        df_dict = get_dfdict_from_filelist(files)

        state_id = insert_inital_pcdata(df_dict)
    except KeyError as e:
        raise InvalidParametersException()
    if not state_id:
        raise NotFoundException(code=400, detail="Pc does Not Exsist")

    return JSONResponse(content={"result": "Data inserted successfully", "state_id": state_id}, status_code=200)



@data.post("/", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def ingest_data(files: list[UploadFile], stateId: int):
    """
    **Insert Timeseries data.**
    **Args:**
        stateId (int): The ID of the state.
        files (list[UploadFile]): A list of UploadFile objects representing the Timeseries data files.
            - File names must include: "application", "connection", "resources", "network".
    **Returns:**
        dict:
        A dictionary with a 'result' key indicating the success or failure of the operation,
        'pcdata_id' the ID of the pcData inserted,
        and 'Anomalies found' indicating the number of anomalies detected.
    """
    try:
        df_map = get_dfdict_from_filelist(files)

        pcdata = df_map["resources"]
        application_data = df_map["application"]

        pc_total_df, anomaly_list = requests.preprocess_pc_data(df_map["application"], stateId)
        print(anomaly_list)

        pcdata_id = insert_running_pcdata(stateId, df_map, pc_total_df, anomaly_list)

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": pcdata_id}, status_code=200)
    except KeyError as e:
        raise InvalidParametersException()
