from abc import ABC, abstractmethod
from typing import Iterable, Optional

from services.postgres.tables import Place


class AbstractPlaceRepository(ABC):

    @abstractmethod
    async def create(self, place: Place) -> Place:
        ...

    @abstractmethod
    async def get(self, place_id: int) -> Optional[Place]:
        ...

    @abstractmethod
    async def list(
        self,
        place_id: int | None = None,
        name: str | None = None,
        category: str | None = None,
        city: str | None = None,
    ) -> Iterable[Place]:
        ...

    @abstractmethod
    async def update(
        self,
        *,
        place_id: int | None = None,
        name: str | None = None,
        category: str | None = None,
        city: str | None = None,
        new_name: str | None = None,
        new_category: str | None = None,
        new_city: str | None = None,
    ) -> int:
        ...

    @abstractmethod
    async def delete(self, place_id: int) -> None:
        ...
