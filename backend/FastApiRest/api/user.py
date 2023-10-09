from typing import List

import psycopg2
from fastapi import HTTPException, APIRouter

from db_access.user import get_users, add_user, check_login, IdentifierType, get_all_user_alerts
from api.helper import gen_salt
from exceptions.DataBaseExcepion import DataBaseException
from exceptions.WrongLoginException import WrongLoginException
from model.data import AlertData

from model.user import CheckLoginRequest, AddUserRequest, UserAlerts

user = APIRouter()


@user.get('/', response_model=list, tags=["User"])
def get_all_users():
    """
    Get all users.

    Returns:
        list: A list of user dictionaries.
    """
    return get_users()


@user.post('/check_login', response_model=dict, tags=["User"])
def check_login_api(data: CheckLoginRequest):
    """
    Check user login credentials.

    Args:
        data (CheckLoginRequest): The login credentials.

    Returns:
        dict: A dictionary with 'valid_login' and 'user_id' keys.
    """
    valid_login, user_id = False, None

    if data.email:
        valid_login, user_id = check_login(data.email, IdentifierType.EMAIL, data.password)
    elif data.user_id:
        valid_login, user_id = check_login(data.user_id, IdentifierType.ID, data.password)
    elif data.name:
        valid_login, user_id = check_login(data.name, IdentifierType.NAME, data.password)
    else:
        raise HTTPException(status_code=400, detail='Invalid request')

    if not valid_login or not user_id:
        raise WrongLoginException()

    response_data = {'valid_login': valid_login, 'user_id': user_id}
    return response_data


@user.post('/add_user', response_model=dict, status_code=201, tags=["User"])
def add_user_api(data: AddUserRequest):
    """
    Add a new user.

    Args:
        data (AddUserRequest): The user data to add.

    Returns:
        dict: A dictionary with a 'user_id' key containing the newly inserted user ID.
    """
    salt = gen_salt()

    user_id = add_user(data.name, data.email, data.password, salt)
    if user_id == -1:
        raise HTTPException(status_code=500, detail='Failed to insert user.')

    return {'user_id': user_id}
