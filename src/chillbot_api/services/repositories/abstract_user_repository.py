from abc import ABC, abstractmethod
from typing import Iterable, Optional

from services.postgres.tables import User


class AbstractUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> User:
        ...

    @abstractmethod
    async def get(self, user_id: int) -> Optional[User]:
        ...

    @abstractmethod
    async def list(
        self,
        user_id: int | None = None,
        tg_id: int | None = None,
        is_admin: bool | None = None,
    ) -> Iterable[User]:
        ...

    @abstractmethod
    async def update(
        self,
        *,
        user_id: int | None = None,
        tg_id: int | None = None,
        is_admin: bool | None = None,
        new_tg_id: int | None = None,
        new_is_admin: bool | None = None,
    ) -> int:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...
