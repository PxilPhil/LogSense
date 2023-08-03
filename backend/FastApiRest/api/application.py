from typing import Optional

from fastapi import APIRouter, HTTPException, Body
from data_analytics import requests
from db_access.application import get_application, get_application_list, get_grouped_by_interval_application
from model.data import ApplicationData, ApplicationListObject
from model.pc import PCItem

application = APIRouter()


@application.get("/{application_name}/", response_model=ApplicationData, tags=["Application"])
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
    try:
        df, data_list = get_application(pc_id, application_name, start, end)
        if df is None:
            return None
        df, event_list, anomaly_list, standard_deviation, mean = requests.analyze_application_data(df, application_name)
        print(anomaly_list)
        application_data = ApplicationData(
            pc=pc_id,
            application_name=application_name,
            standard_deviation=standard_deviation,
            mean=mean,
            time_series_data=data_list,
            event_list=event_list,
            anomaly_list=anomaly_list
        )

        return application_data
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")


# no idea if this works haha
@application.get("/{application_name}/bucket", response_model=dict, tags=["Application"])
def fetch_application_buckets(pc_id: int, application_name: str, start: str, end: str, bucket_value: str):
    """
    Get Data to Application

    Parameters:
        application_name (str): Name of the Application
        start (int): Start value
        end (int): End value

    Returns:
        dict: A dictionary with PC ID, Application Name, Start, and End values
        :param bucket_value:
    """
    try:
        df, data_list = get_grouped_by_interval_application(pc_id, application_name, start, end, bucket_value, None)
        if df is None:
            return None

        return {'data_list': data_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")


@application.get("/", response_model=ApplicationListObject, tags=["Application"])
def fetch_application_list(pc_id: int, start: str, end: str):
    """
    Get a list of running applications on the pc

    Parameters:
        pc_id (int): ID of the PC

    Returns:
        dict: A dictionary with PC ID
        :param end:
        :param start:
    """
    try:
        application_list = get_application_list(pc_id, start, end)
        application_list_obj = ApplicationListObject(
            pc_id=pc_id,
            start=start,
            end=end,
            application_list=application_list
        )
        print(application_list_obj)
        return application_list_obj
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
