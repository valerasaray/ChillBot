from abc import ABC, abstractmethod
from typing import Iterable, Optional

from services.postgres.tables import User


class AbstractUserRepository(ABC):

    @abstractmethod
    async def create(
        self,
        tg_id: int,
        is_admin: bool
    ) -> User:
        ...

    @abstractmethod
    async def get(self, user_id: int) -> Optional[User]:
        ...

    @abstractmethod
    async def list(
        self,
        tg_id: int | None = None,
        is_admin: bool | None = None,
    ) -> Iterable[User]:
        ...

    @abstractmethod
    async def update(
        self,
        user_id: int,
        tg_id: int | None = None,
        is_admin: bool | None = None,
    ) -> int:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...
