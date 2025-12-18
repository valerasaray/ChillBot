from abc import ABC, abstractmethod
from typing import Iterable, Optional

from services.postgres.tables import Rate


class AbstractRateRepository(ABC):

    @abstractmethod
    async def create(
        self,
        rate: int,
        user_id: int,
        place_id: int
    ) -> Rate:
        ...

    @abstractmethod
    async def get(self, rate_id: int) -> Optional[Rate]:
        ...

    @abstractmethod
    async def list(
        self,
        rate: int | None = None,
        user_id: int | None = None,
        place_id: int | None = None
    ) -> Iterable[Rate]:
        ...

    @abstractmethod
    async def update(
        self,
        rate_id: int,
        rate: int | None = None,
        user_id: int | None = None,
        place_id: int | None = None
    ) -> int:
        ...

    @abstractmethod
    async def delete(self, rate_id: int) -> None:
        ...
