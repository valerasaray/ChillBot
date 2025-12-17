from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.tables import Rate
from services.repositories.abstract_rate_repository import AbstractRateRepository


class PostgresRateRepository(AbstractRateRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, rate: Rate) -> Rate:
        self._session.add(rate)
        await self._session.commit()
        return rate

    async def get(self, rate_id: str):
        return await self._session.get(Rate, rate_id)

    async def list(self, rate_id=None, user_id=None, place_id=None, rate=None):
        stmt = select(Rate)

        if rate_id is not None:
            stmt = stmt.where(Rate.rate_id == rate_id)
        if user_id is not None:
            stmt = stmt.where(Rate.user_id == user_id)
        if place_id is not None:
            stmt = stmt.where(Rate.place_id == place_id)
        if rate is not None:
            stmt = stmt.where(Rate.rate == rate)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(self, **filters):
        stmt = update(Rate)

        for field in ("rate_id", "user_id", "place_id", "rate"):
            value = filters.get(field)
            if value is not None:
                stmt = stmt.where(getattr(Rate, field) == value)

        if filters.get("new_rate") is not None:
            stmt = stmt.values(rate=filters["new_rate"])

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def delete(self, rate_id: str):
        await self._session.execute(
            delete(Rate).where(Rate.rate_id == rate_id)
        )
        await self._session.commit()
