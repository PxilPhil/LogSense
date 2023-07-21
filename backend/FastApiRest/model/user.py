from pydantic import BaseModel
from typing import List


class CheckLoginRequest(BaseModel):
    email: str = None
    user_id: str = None
    name: str = None
    password: str


class AddUserRequest(BaseModel):
    name: str
    email: str
    password: str
