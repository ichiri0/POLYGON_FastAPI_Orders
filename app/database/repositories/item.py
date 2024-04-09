"""
Репозиторий для Item.
"""

from datetime import datetime as dt
from datetime import timedelta as td

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from .. import models


class ItemRepo(Repository[models.Item]):
    type_model: type[models.Item]

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.Item, session=session)

    async def new(
        self,
        name: str,
        description: str,
    ) -> models.Item:
        model = models.Item()
        model.name = name
        model.description = description

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry

    async def get_by_id(self, id: int) -> models.Item:
        where_clause = [self.type_model.id == id]
        entry = await self.get_by_where(where_clause)
        return entry
