from fastapi import APIRouter, HTTPException, Body
from starlette.responses import JSONResponse

from data_analytics.requests import check_for_alerts
from db_access.alerts import injestCustomAlerts, getCustomAlerts
from model.alerts import CustomAlerts, IngestCustomAlert

alerts = APIRouter()

# 1 - get all
@alerts.get("/{user_id}", response_model=dict, tags=["Alerts"])
def fetch_alerts(user_id: int, start: str, end: str):
    """
    Returns all alerts that have occured in the specified timeframe, both standardized alerts and custom user alerts
    :param end:
    :param start:
    :param user_id:
    :return:
    """
    detected_alerts = check_for_alerts(user_id, start, end)
    return JSONResponse(content=detected_alerts)

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
    return JSONResponse(content={"detail": "anomalies inserted successfully", "anomaly_id": anomaly_id}, status_code=200)


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
