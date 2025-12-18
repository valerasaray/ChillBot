from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.tables import User
from services.repositories.abstract_user_repository import AbstractUserRepository


class PostgresUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        tg_id: int,
        is_admin: bool
    ) -> User:
        user = User(
            tg_id=tg_id,
            is_admin=is_admin
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get(self, user_id: int):
        return await self._session.get(User, user_id)

    async def list(
        self,
        tg_id: int | None = None,
        is_admin: bool | None = None,
    ):
        stmt = select(User)

        if tg_id is not None:
            stmt = stmt.where(User.tg_id == tg_id)
        if is_admin is not None:
            stmt = stmt.where(User.is_admin == is_admin)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(
        self,
        user_id: int,
        tg_id: int | None = None,
        is_admin: bool | None = None,
    ) -> int:
        values = {}

        if tg_id is not None:
            values["tg_id"] = tg_id
        if is_admin is not None:
            values["is_admin"] = is_admin

        if not values:
            return 0

        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(**values)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def delete(self, user_id: int) -> None:
        await self._session.execute(
            delete(User).where(User.user_id == user_id)
        )
        await self._session.commit()
