from fastapi import APIRouter, HTTPException, Body
from data_analytics import requests
from db_access.application import get_application

from model.pc import PCItem

application = APIRouter()


@application.get("/{application_name}/", tags=["Application"])
def fetch_application(pc_id: int, application_name: str, start: str, end: str):
    """
    Get Data to Application

    Parameters:
        application_name (str): Name of the Application
        start (int): Start value
        end (int): End value

    Returns:
        dict: A dictionary with PC ID, Application Name, Start, and End values
    """
    df, data_list = get_application(pc_id, application_name, start, end)
    #df, anomaly_list = requests.fetch_application_data(application_name)
    print(df)
    print(data_list)
    # TODO: The way all gets should return time series data is in form of arrays
    return {"pc": pc_id, "application": application_name, "start": start, "end": end}


@application.get("/", tags=["Application"])
def get_application_list(pc_id: int, start: int, end: int):
    """
    Get a list of running applications on the pc

    Parameters:
        pc_id (int): ID of the PC

    Returns:
        dict: A dictionary with PC ID
    """
    # TODO: Return List of Applications from DB
    return {"pc": pc_id, "start": start, "end": end}
