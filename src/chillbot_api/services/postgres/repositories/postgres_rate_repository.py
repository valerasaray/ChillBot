from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.tables import Rate
from services.repositories.abstract_rate_repository import AbstractRateRepository


class PostgresRateRepository(AbstractRateRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        rate: int,
        user_id: int,
        place_id: int
    ) -> Rate:
        rate_obj = Rate(
            rate=rate,
            user_id=user_id,
            place_id=place_id
        )
        self._session.add(rate_obj)
        await self._session.commit()
        await self._session.refresh(rate_obj)
        return rate_obj

    async def get(self, rate_id: int):
        return await self._session.get(Rate, rate_id)

    async def list(
        self,
        rate: int | None = None,
        user_id: int | None = None,
        place_id: int | None = None
    ):
        stmt = select(Rate)

        if rate is not None:
            stmt = stmt.where(Rate.rate == rate)
        if user_id is not None:
            stmt = stmt.where(Rate.user_id == user_id)
        if place_id is not None:
            stmt = stmt.where(Rate.place_id == place_id)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(
        self,
        rate_id: int,
        rate: int | None = None,
        user_id: int | None = None,
        place_id: int | None = None
    ) -> int:
        values = {}

        if rate is not None:
            values["rate"] = rate
        if user_id is not None:
            values["user_id"] = user_id
        if place_id is not None:
            values["place_id"] = place_id

        if not values:
            return 0

        stmt = (
            update(Rate)
            .where(Rate.rate_id == rate_id)
            .values(**values)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def delete(self, rate_id: int) -> None:
        await self._session.execute(
            delete(Rate).where(Rate.rate_id == rate_id)
        )
        await self._session.commit()
