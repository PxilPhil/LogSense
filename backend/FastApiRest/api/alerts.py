from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Body
from starlette.responses import JSONResponse

from data_analytics.justification import justify_pc_data_points
from data_analytics.requests import check_for_alerts
from db_access.alerts import injestCustomAlerts, getCustomAlerts
from db_access.pc import get_total_pc_application_data_between
from model.alerts import CustomAlerts, IngestCustomAlert, AlertNotification
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
    pc_df, pc_data_list = get_total_pc_application_data_between(user_id, start, end)
    found_custom_alerts = getCustomAlerts(user_id)
    alert_notifications = check_for_alerts(user_id, found_custom_alerts.custom_alert_list, pc_df, start, end)
    return alert_notifications


@alerts.get("/explain", response_model=list[Justification], tags=["Alerts"])
def explain(alert_notification: AlertNotification):
    """
    Returns the justifications for a certain timestamp (the client sends this request when it wants to know details about alerts or events)
    :param alert_notification:
    :return:
    """
    timestamps: List[datetime] = alert_notification.detected_alert_list
    justifications: list[Justification] = justify_pc_data_points(None, timestamps, None, 1, False)
    return None


@alerts.get("/all/{user_id}", tags=["Alerts"], response_model=IngestCustomAlert, responses={
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
def add_custom_alert(alerts: CustomAlerts = Body(...)):
    anomaly_id = injestCustomAlerts(alerts)
    return JSONResponse(content={"detail": "anomalies inserted successfully", "anomaly_id": anomaly_id},
                        status_code=200)


# 3 - delete
@alerts.delete("/", tags=["Alerts"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def delete_custom_alert():
    raise NotImplemented


# 4 - update (put to )
@alerts.put("/", tags=["Alerts"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def update_custom_alert():
    raise NotImplemented
