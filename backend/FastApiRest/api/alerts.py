from fastapi import APIRouter, HTTPException, Body
from starlette.responses import JSONResponse

from db_access.alerts import injestCustomAlerts, getCustomAlerts
from model.alerts import CustomAlerts, InjestCustomAlerts

alerts = APIRouter()

# 1 - get all
@alerts.get("/", tags=["Alerts"], response_model=InjestCustomAlerts, responses={
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
