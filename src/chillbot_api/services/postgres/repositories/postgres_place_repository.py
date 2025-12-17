from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.tables import Place
from services.repositories.abstract_place_repository import AbstractPlaceRepository


class PostgresPlaceRepository(AbstractPlaceRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, place: Place) -> Place:
        self._session.add(place)
        await self._session.commit()
        return place

    async def get(self, place_id: int):
        return await self._session.get(Place, place_id)

    async def list(self, place_id=None, name=None, category=None, city=None):
        stmt = select(Place)

        if place_id is not None:
            stmt = stmt.where(Place.place_id == place_id)
        if name is not None:
            stmt = stmt.where(Place.name == name)
        if category is not None:
            stmt = stmt.where(Place.category == category)
        if city is not None:
            stmt = stmt.where(Place.city == city)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(self, **filters):
        stmt = update(Place)

        for field in ("place_id", "name", "category", "city"):
            value = filters.get(field)
            if value is not None:
                stmt = stmt.where(getattr(Place, field) == value)

        values = {
            k.replace("new_", ""): v
            for k, v in filters.items()
            if k.startswith("new_") and v is not None
        }

        result = await self._session.execute(stmt.values(**values))
        await self._session.commit()
        return result.rowcount

    async def delete(self, place_id: int):
        await self._session.execute(
            delete(Place).where(Place.place_id == place_id)
        )
        await self._session.commit()
