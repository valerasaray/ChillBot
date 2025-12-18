from abc import ABC, abstractmethod
from typing import Iterable, Optional

from services.postgres.tables import Place


class AbstractPlaceRepository(ABC):

    @abstractmethod
    async def create(
        self,
        name: str,
        category: str,
        city: str
    ) -> Place:
        ...

    @abstractmethod
    async def get(self, place_id: int) -> Optional[Place]:
        ...

    @abstractmethod
    async def list(
        self,
        name: str | None = None,
        category: str | None = None,
        city: str | None = None,
    ) -> Iterable[Place]:
        ...

    @abstractmethod
    async def update(
        self,
        place_id: int,
        name: str | None = None,
        category: str | None = None,
        city: str | None = None,
    ) -> int:
        ...

    @abstractmethod
    async def delete(self, place_id: int) -> None:
        ...
