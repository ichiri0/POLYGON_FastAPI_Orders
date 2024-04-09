"""
Репозиторий для OrderItem.
"""

from datetime import datetime as dt
from datetime import timedelta as td

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from .. import models


class OrderItemRepo(Repository[models.OrderItem]):
    type_model: type[models.OrderItem]

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.OrderItem, session=session)

    async def new(
        self,
        order_fk: int,
        item_fk: int,
    ) -> models.OrderItem:
        model = models.OrderItem()
        model.order_fk = order_fk
        model.item_fk = item_fk

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry
    
    async def get_by_id(self, id: int) -> models.OrderItem:
        where_clause = [self.type_model.id == id]
        entry = await self.get_by_where(where_clause)
        return entry

    async def get_all(self) -> list[models.OrderItem]:
        where_clause = [
        ]
        entry = await self.get_many(where_clause)
        return entry
    
    async def get_many_by_order(self, order_fk: int) -> list[models.OrderItem]:
        where_clause = [
            self.type_model.order_fk == order_fk,
        ]
        entry = await self.get_many(where_clause)
        return entry

    async def get_many_by_item(self, item_fk: int) -> list[models.OrderItem]:
        where_clause = [
            self.type_model.item_fk == item_fk,
        ]
        entry = await self.get_many(where_clause)
        return entry
