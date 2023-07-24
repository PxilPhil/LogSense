from fastapi import APIRouter, HTTPException, Body
from db_access.pc import get_pcs, get_pcs_by_userid, add_pc

from model.pc import PCItem


application = APIRouter()

@application.get("/{application_name}", tags=["Application"])
def get_application(pc_id: int, application_name: str):
    """
    Get PC and Application IDs

    Parameters:
        pc_id (int): ID of the PC
        application_name (str): name of the Application

    Returns:
        dict: A dictionary with PC and Application IDs
    """
    return {"pc": pc_id, "application": application_name}

@application.get("/", tags=["Application"])
def get_application(pc_id: int):
    """
    Get PC and Application IDs

    Parameters:
        pc_id (int): ID of the PC
        application_id (int): ID of the Application

    Returns:
        dict: A dictionary with PC and Application IDs
    """
    return {"pc": pc_id}


