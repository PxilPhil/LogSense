from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

data = APIRouter()

class TimeseriesData(BaseModel):
    pcdata: str
    other_field: int

@data.post("/", description="Insert Timeseries data", tags=["Data"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid JSON data"},
    500: {"description": "Internal server error"}
})
def injest_all_data(request: Request, data: TimeseriesData):
    """
    Insert Timeseries data.

    Args:
        request (Request): The FastAPI request object.
        data (TimeseriesData): The Timeseries data to insert.

    Returns:
        dict: A dictionary with a 'result' key indicating the success or failure of the operation.
    """
    try:
        pcdata = data.pcdata
        other_field = data.other_field


        if True:
            error_data = {'error': 'not implemented yet'}
            return JSONResponse(content=error_data, status_code=500)

        return {"result": "Data inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")