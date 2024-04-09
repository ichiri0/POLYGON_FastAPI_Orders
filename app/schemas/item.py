"""
Схемы для пользователя.
"""

from pydantic import BaseModel
from datetime import datetime as dt

class NewItem(BaseModel):
    name: str = "name"
    description: str = "description"

    class Config:
        from_attributes = True


class Item(BaseModel):
    id: int = 1
    name: str = "name"
    description: str = "description"

    class Config:
        from_attributes = True
