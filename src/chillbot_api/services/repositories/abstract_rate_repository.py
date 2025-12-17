from abc import ABC, abstractmethod
from typing import Iterable, Optional

from services.postgres.tables import Rate


class AbstractRateRepository(ABC):

    @abstractmethod
    async def create(self, rate: Rate) -> Rate:
        ...

    @abstractmethod
    async def get(self, rate_id: str) -> Optional[Rate]:
        ...

    @abstractmethod
    async def list(
        self,
        rate_id: str | None = None,
        user_id: int | None = None,
        place_id: int | None = None,
        rate: int | None = None,
    ) -> Iterable[Rate]:
        ...

    @abstractmethod
    async def update(
        self,
        *,
        rate_id: str | None = None,
        user_id: int | None = None,
        place_id: int | None = None,
        rate: int | None = None,
        new_rate: int | None = None,
    ) -> int:
        ...

    @abstractmethod
    async def delete(self, rate_id: str) -> None:
        ...
