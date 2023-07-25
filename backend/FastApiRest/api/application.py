from fastapi import APIRouter, HTTPException, Body
from data_analytics import requests
from db_access.pc import get_pcs, get_pcs_by_userid, add_pc

from model.pc import PCItem


application = APIRouter()

@application.get("/{application_name}/", tags=["Application"])
def get_application(pc_id: int, application_name: str, start: int, end: int):
    """
    Get Data to Application

    Parameters:
        application_name (str): Name of the Application
        start (int): Start value
        end (int): End value

    Returns:
        dict: A dictionary with PC ID, Application Name, Start, and End values
    """
    df, anomaly_list = requests.fetch_application_data(application_name)
    print(df)
    print(anomaly_list)
    return {"pc": pc_id, "application": application_name, "start": start, "end": end}

@application.get("/", tags=["Application"])
def get_application(pc_id: int, start: int, end: int):
    """
    Get all info to application

    Parameters:
        pc_id (int): ID of the PC

    Returns:
        dict: A dictionary with PC ID
    """
    return {"pc": pc_id, "start": start, "end": end}


