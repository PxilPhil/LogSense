from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from model.data import TimeseriesData, PCData, ApplicationData, NetworkInterface

from db_access.data import insert_pcdata


data = APIRouter()

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

        pcdata_id = insert_pcdata(pcdata)

        return JSONResponse(content={"result": "Data inserted successfully", "pcdata_id": pcdata_id}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
