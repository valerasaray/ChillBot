from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.tables import User
from services.repositories.abstract_user_repository import AbstractUserRepository


class PostgresUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        return user

    async def get(self, user_id: int):
        return await self._session.get(User, user_id)

    async def list(self, user_id=None, tg_id=None, is_admin=None):
        stmt = select(User)

        if user_id is not None:
            stmt = stmt.where(User.user_id == user_id)
        if tg_id is not None:
            stmt = stmt.where(User.tg_id == tg_id)
        if is_admin is not None:
            stmt = stmt.where(User.is_admin == is_admin)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(self, **filters):
        stmt = update(User)

        for field in ("user_id", "tg_id", "is_admin"):
            value = filters.get(field)
            if value is not None:
                stmt = stmt.where(getattr(User, field) == value)

        values = {}
        if filters.get("new_tg_id") is not None:
            values["tg_id"] = filters["new_tg_id"]
        if filters.get("new_is_admin") is not None:
            values["is_admin"] = filters["new_is_admin"]

        result = await self._session.execute(stmt.values(**values))
        await self._session.commit()
        return result.rowcount

    async def delete(self, user_id: int):
        await self._session.execute(
            delete(User).where(User.user_id == user_id)
        )
        await self._session.commit()
