"""
Связующая таблица Order и Item.
"""

from datetime import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class OrderItem(Base):
    order_fk: Mapped[int] = mapped_column(
        sa.ForeignKey("order.id"), unique=False, nullable=False
    )
    item_fk: Mapped[int] = mapped_column(
        sa.ForeignKey("item.id"), unique=False, nullable=False
    )

    def __repr__(self):
        return f"OrderItem:{self.id=}"