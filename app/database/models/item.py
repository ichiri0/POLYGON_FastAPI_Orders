"""
Представление Item.
"""

from datetime import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Item(Base):
    name: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    description: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)

    def __repr__(self):
        return f"Item:{self.id=}"