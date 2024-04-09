"""
Схемы для пользователя.
"""

from pydantic import BaseModel
from datetime import datetime as dt

class NewOrder(BaseModel):
    client_id: int = 1
    address: str = "string"
    created_at: dt
    created_by_microservice_id: str

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: int = 1
    client_id: int = 1
    address: str = "string"
    created_at: dt
    created_by_microservice_id: str

    class Config:
        from_attributes = True
