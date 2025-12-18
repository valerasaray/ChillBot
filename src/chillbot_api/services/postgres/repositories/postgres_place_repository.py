from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.tables import Place
from services.repositories.abstract_place_repository import AbstractPlaceRepository


class PostgresPlaceRepository(AbstractPlaceRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        name: str,
        category: str,
        city: str
    ) -> Place:
        place = Place(
            name=name,
            category=category,
            city=city
        )
        self._session.add(place)
        await self._session.commit()
        await self._session.refresh(place)
        return place

    async def get(self, place_id: int):
        return await self._session.get(Place, place_id)

    async def list(
        self,
        name: str | None = None,
        category: str | None = None,
        city: str | None = None,
    ):
        stmt = select(Place)

        if name is not None:
            stmt = stmt.where(Place.name == name)
        if category is not None:
            stmt = stmt.where(Place.category == category)
        if city is not None:
            stmt = stmt.where(Place.city == city)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(
        self,
        place_id: int,
        name: str | None = None,
        category: str | None = None,
        city: str | None = None,
    ) -> int:
        values = {}

        if name is not None:
            values["name"] = name
        if category is not None:
            values["category"] = category
        if city is not None:
            values["city"] = city

        if not values:
            return 0

        stmt = (
            update(Place)
            .where(Place.place_id == place_id)
            .values(**values)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def delete(self, place_id: int) -> None:
        await self._session.execute(
            delete(Place).where(Place.place_id == place_id)
        )
        await self._session.commit()
