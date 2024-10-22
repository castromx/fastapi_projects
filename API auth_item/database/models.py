from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

metadata = MetaData()

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column(default=True)

    items: Mapped[int] = relationship('ItemModel', back_populates='owner')


class ItemModel(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    owner: Mapped[str] = relationship('UserModel', back_populates='items')
