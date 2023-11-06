from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Body
from starlette.responses import JSONResponse

from data_analytics.justification import justify_pc_data_points, justify_application_data_points
from data_analytics.requests import check_for_alerts
from db_access.alerts import ingestCustomAlerts, getCustomAlerts, deleteCustomAlerts
from db_access.pc import get_ram_time_series_between, get_total_pc_data
from model.alerts import CustomAlerts, IngestCustomAlert, AlertNotification, CustomAlert
from model.data import Justification

alerts = APIRouter()


# 1 - get all
@alerts.get("/{user_id}", response_model=List[AlertNotification], tags=["Alerts"])
def fetch_alerts(user_id: int, start: str, end: str):
    """
    Returns all alerts that have occured in the specified timeframe, both standardized alerts and custom user alerts
    :param end:
    :param start:
    :param user_id:
    :return:
    """
    pc_df = get_total_pc_data(user_id, start, end)
    found_custom_alerts = getCustomAlerts(user_id)
    alert_notifications = check_for_alerts(user_id, found_custom_alerts.custom_alert_list, pc_df, start, end)
    return alert_notifications


@alerts.get("/justify/{pc_id}", response_model=list[Justification], tags=["Alerts"])
def justify_application(timestamps: list[datetime], pc_id: int, application: Optional[str] = None):
    """
    Returns the justifications for a certain timestamp (the client sends this request when it wants to know details about alerts or events)
    :param pc_id:
    :param application_name:
    :param timestamps:
    :return:
    """
    justifications: list[Justification] = []
    if application:
        justifications = justify_application_data_points(timestamps, application, pc_id)
    else:
        justifications = justify_pc_data_points(None, timestamps, justifications, pc_id, False)
    return justifications


@alerts.get("/all/{user_id}", tags=["Alerts"], response_model=CustomAlerts, responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def get_all_alerts(user_id: int):
    return getCustomAlerts(user_id)


# 2 - add custom
@alerts.post("/", tags=["Alerts"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def add_custom_alert(alert: CustomAlert):
    # make every "empty" into null
    for condition in alert.conditions:
        if condition.absolute_trigger_value == "":
            condition.absolute_trigger_value = None
        if condition.percentage_trigger_value == "":
            condition.percentage_trigger_value = None
        if condition.application == "":
            condition.application = None
    if (condition.percentage_trigger_value == None and condition.absolute_trigger_value == None) or condition.column == None or condition.column == "":
        return JSONResponse(content={"detail": "Alert had no meaningful trigger values", "anomaly_id": 0}, status_code=404)
    anomaly_id = ingestCustomAlerts(alert)
    return JSONResponse(content={"detail": "Alert inserted successfully", "anomaly_id": anomaly_id}, status_code=200)

# 3 - delete
@alerts.delete("/{alert_id}", tags=["Alerts"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def delete_custom_alert(alert_id: int):
    success, message = deleteCustomAlerts(alert_id)
    if success:
        return JSONResponse(content={"detail": message, "anomaly_id": alert_id},
                        status_code=200)
    else:
        return JSONResponse(content={"detail": message},  status_code=500)