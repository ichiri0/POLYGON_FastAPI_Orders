"""
Представление Order.
"""

from datetime import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Order(Base):
    client_id: Mapped[int] = mapped_column(sa.BigInteger, unique=False, nullable=False)
    address: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    created_at: Mapped[str] = mapped_column(sa.DateTime, unique=False, default=dt.now())
    create_by_microservice_id: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)

    def __repr__(self):
        return f"Order:{self.id=}"
