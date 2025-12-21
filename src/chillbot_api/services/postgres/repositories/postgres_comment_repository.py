from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.tables import Comment
from services.repositories.abstract_comment_repository import AbstractCommentRepository


class PostgresCommentRepository(AbstractCommentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        text: str,
        is_moderated: bool,
        user_id: int,
        place_id: int
    ) -> Comment:
        comment = Comment(
            text=text,
            is_moderated=is_moderated,
            user_id=user_id,
            place_id=place_id
        )
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment)
        return comment

    async def get(self, comment_id: int):
        return await self._session.get(Comment, comment_id)

    async def list(
        self,
        limit: int = 100,
        text: str | None = None,
        is_moderated: bool | None = None,
        user_id: int | None = None,
        place_id: int | None = None,
        last_comment_id: int | None = None
    ):
        stmt = select(Comment)
            
        if text is not None:
            stmt = stmt.where(Comment.text == text)
        if is_moderated is not None:
            stmt = stmt.where(Comment.is_moderated == is_moderated)
        if user_id is not None:
            stmt = stmt.where(Comment.user_id == user_id)
        if place_id is not None:
            stmt = stmt.where(Comment.place_id == place_id)
        
        if last_comment_id is not None:
            stmt = stmt.where(Comment.comment_id > last_comment_id)
        
        stmt = stmt.order_by(Comment.comment_id.asc()).limit(limit)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(
        self, 
        comment_id: int,
        is_moderated: bool | None = None,
        user_id: int | None = None,
        place_id: int | None = None,
        text: str | None = None,
    ):
        values = {}

        if is_moderated is not None:
            values["is_moderated"] = is_moderated
        if user_id is not None:
            values["user_id"] = user_id
        if place_id is not None:
            values["place_id"] = place_id
        if text is not None:
            values["text"] = text
            
        stmt = (
            update(Comment)
            .where(Comment.comment_id == comment_id)
            .values(**values)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount

    async def delete(self, comment_id: str):
        await self._session.execute(
            delete(Comment).where(Comment.comment_id == comment_id)
        )
        await self._session.commit()
