from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.tables import Comment
from services.repositories.abstract_comment_repository import AbstractCommentRepository


class PostgresCommentRepository(AbstractCommentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, comment: Comment) -> Comment:
        self._session.add(comment)
        await self._session.commit()
        return comment

    async def get(self, comment_id: str):
        return await self._session.get(Comment, comment_id)

    async def list(self, comment_id=None, is_moderated: bool | None = None, user_id=None, place_id=None):
        stmt = select(Comment)

        if comment_id is not None:
            stmt = stmt.where(Comment.comment_id == comment_id)
        if is_moderated is not None:
            stmt = stmt.where(Comment.is_moderated == is_moderated)
        if user_id is not None:
            stmt = stmt.where(Comment.user_id == user_id)
        if place_id is not None:
            stmt = stmt.where(Comment.place_id == place_id)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(self, **filters):
        stmt = update(Comment)

        for field in ("comment_id", "is_moderated", "user_id", "place_id"):
            value = filters.get(field)
            if value is not None:
                stmt = stmt.where(getattr(Comment, field) == value)

        if filters.get("new_text") is not None:
            stmt = stmt.values(text=filters["new_text"])

        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def delete(self, comment_id: str):
        await self._session.execute(
            delete(Comment).where(Comment.comment_id == comment_id)
        )
        await self._session.commit()
