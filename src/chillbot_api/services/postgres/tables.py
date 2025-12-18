from sqlalchemy import BigInteger, Numeric, String, ForeignKey, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseTable(DeclarativeBase):
    pass


class User(BaseTable):
    __tablename__ = 'User'
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    is_admin: Mapped[bool] = mapped_column(Boolean)


class Place(BaseTable):
    __tablename__ = 'Place'
    place_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)


class Comment(BaseTable):
    __tablename__ = 'Comment'
    comment_id: Mapped[str] = mapped_column(String, primary_key=True)
    text: Mapped[str] = mapped_column(String)
    is_moderated: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    place_id: Mapped[int] = mapped_column(ForeignKey('place.place_id'))


class Rate(BaseTable):
    __tablename__ = 'Rate'
    rate_id: Mapped[str] = mapped_column(String, primary_key=True)
    rate: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    place_id: Mapped[int] = mapped_column(ForeignKey('place.place_id'))
