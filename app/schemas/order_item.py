"""
Схемы для пользователя.
"""

from pydantic import BaseModel
from datetime import datetime as dt
from ..schemas import Order, Item

class NewOrderItem(BaseModel):
    order_id: int = 1
    item_id: int = 1

    class Config:
        from_attributes = True


class OrderItem(BaseModel):
    id: int = 1
    order_id: Order
    item_id: Item

    class Config:
        from_attributes = True
