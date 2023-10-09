from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Body

from data_analytics import requests
from exceptions.InvalidParametersException import InvalidParametersException
from db_access.application import get_application_between, get_application_list, get_grouped_by_interval_application, \
    select_total_running_time_application
from exceptions.NotFoundExcepion import NotFoundException
from model.application import ApplicationData, ApplicationListObject
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
        df, data_list = get_application_between(pc_id, application_name, start, end)
        if df is None:
            raise NotFoundException(code=500, detail="Application was not found.")
        df, ram_events_and_anomalies, cpu_events_and_anomalies, anomaly_measurements_ram, anomaly_measurements_cpu, std_ram, std_cpu, mean_ram, mean_cpu, cov_ram, cov_cpu, stability_ram, stability_cpu = requests.analyze_application_data(df, application_name)
        application_data = ApplicationData(
            pc=pc_id,
            application_name=application_name,
            standard_deviation_ram=std_ram,
            standard_deviation_cpu=std_cpu,
            mean_ram=mean_ram,
            mean_cpu=mean_cpu,
            cov_ram=cov_ram,
            cov_cpu=cov_cpu,
            stability_ram=stability_ram,
            stability_cpu=stability_cpu,
            time_series_data=data_list,
            cpu_events_and_anomalies=cpu_events_and_anomalies,
            ram_events_and_anomalies=ram_events_and_anomalies
        )

        return application_data
    except KeyError as e:
        raise InvalidParametersException()


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
    df, data_list = get_grouped_by_interval_application(pc_id, application_name, start, end, bucket_value, None)
    if df is None:
        raise NotFoundException(code=500, detail="Application was not found.")

    return {'data_list': data_list}


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
    application_list = get_application_list(pc_id, start, end)
    application_list_obj = ApplicationListObject(
        pc_id=pc_id,
        start=start,
        end=end,
        application_list=application_list
    )
    #print(application_list_obj)
    return application_list_obj


@application.get('/{application_name}/time-metrics/', response_model=dict, tags=["Application"])
def get_pc_time_metrics(pc_id: int, application_name: str, start: datetime, end: datetime):
    time_metrics_dict = select_total_running_time_application(start, end, application_name, pc_id)
    return time_metrics_dict