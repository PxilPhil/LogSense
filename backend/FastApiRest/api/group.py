from fastapi import APIRouter, HTTPException, Body

from db_access.pc import get_pcs, get_pcs_by_userid, add_pc

from model.pc import PCItem


group = APIRouter()


@group.get("/", tags=["Group"])
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


@group.get("/{group_id}", tags=["Group"])
def get_application(group_id: int):
    """
    Get PC and Application IDs

    Parameters:
        pc_id (int): ID of the PC
        application_id (int): ID of the Application

    Returns:
        dict: A dictionary with PC and Application IDs
    """
    return {"group": group_id}


