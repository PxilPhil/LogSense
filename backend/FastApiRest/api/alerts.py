from fastapi import APIRouter, HTTPException, Body

alerts = APIRouter()

# 1 - get all
@alerts.get("/", tags=["Alerts"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def get_all_alerts():
    raise NotImplemented


# 2 - add custom
@alerts.post("/", tags=["Alerts"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def add_custom_alert():
    raise NotImplemented


# 3 - delete
@alerts.delete("/", tags=["Alerts"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def add_custom_alert():
    raise NotImplemented

# 4 - update
@alerts.put("/", tags=["Alerts"], responses={
    200: {"description": "Successful response"},
    400: {"description": "Invalid parameters or missing required fields"},
    500: {"description": "Internal server error"}
})
def add_custom_alert():
    raise NotImplemented
