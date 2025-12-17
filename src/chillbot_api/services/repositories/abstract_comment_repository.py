from abc import ABC, abstractmethod
from typing import Iterable, Optional

from services.postgres.tables import Comment


class AbstractCommentRepository(ABC):

    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        ...

    @abstractmethod
    async def get(self, comment_id: str) -> Optional[Comment]:
        ...

    @abstractmethod
    async def list(
        self,
        comment_id: str | None = None,
        user_id: int | None = None,
        place_id: int | None = None,
    ) -> Iterable[Comment]:
        ...

    @abstractmethod
    async def update(
        self,
        *,
        comment_id: str | None = None,
        user_id: int | None = None,
        place_id: int | None = None,
        new_text: str | None = None,
    ) -> int:
        ...

    @abstractmethod
    async def delete(self, comment_id: str) -> None:
        ...
