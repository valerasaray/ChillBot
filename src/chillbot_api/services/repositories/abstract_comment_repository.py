from abc import ABC, abstractmethod
from typing import Iterable, Optional

from services.postgres.tables import Comment


class AbstractCommentRepository(ABC):

    @abstractmethod
    async def create(
        self, 
        text: str,
        is_moderated: bool,
        user_id: int,
        place_id: int
    ) -> Comment:
        ...

    @abstractmethod
    async def get(self, comment_id: int) -> Optional[Comment]:
        ...

    @abstractmethod
    async def list(
        self,
        limit: int = 100,
        offset: int = 0,
        text: int | None = None,
        is_moderated: bool | None = None,
        user_id: int | None = None,
        place_id: int | None = None,
    ) -> Iterable[Comment]:
        ...

    @abstractmethod
    async def update(
        self,
        comment_id: int,
        is_moderated: bool | None = None,
        user_id: int | None = None,
        place_id: int | None = None,
        text: str | None = None,
    ) -> int:
        ...

    @abstractmethod
    async def delete(self, comment_id: int) -> None:
        ...
