"""
Репозиторий для Order.
"""

from datetime import datetime as dt
from datetime import timedelta as td

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from .. import models


class OrderRepo(Repository[models.Order]):
    type_model: type[models.Order]

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.Order, session=session)

    async def new(
        self,
        client_id: int,
        address: str,
        created_at: dt,
        created_by_microservice_id: str,
    ) -> models.Order:
        model = models.Order()
        model.client_id = client_id
        model.address = address
        model.create_at = created_at
        model.create_by_microservice_id = created_by_microservice_id

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry

    async def get_by_id(self, id: int) -> models.Order:
        where_clause = [self.type_model.id == id]
        entry = await self.get_by_where(where_clause)
        return entry

    async def get_by_client_id(self, client_id: int) -> models.Order:
        where_clause = [self.type_model.client_id == client_id]
        entry = await self.get_by_where(where_clause)
        return entry

    async def get_many_by_client(self, client_id: int) -> list[models.Order]:
        where_clause = [
            self.type_model.client_id == client_id,
        ]
        entry = await self.get_many(where_clause)
        return entry
