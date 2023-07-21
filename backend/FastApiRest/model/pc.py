from pydantic import BaseModel
from typing import List


class PCItem(BaseModel):
    user_id: str
    hardware_uuid: str
    client_name: str
    manufacturer: str = None
    model: str = None