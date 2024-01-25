from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Таблиці баз данних

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    email = Column(String, index=True)
    active = Column(Boolean, default=True)

    items = relationship('ItemModel', back_populates='owner')
    # У користувача є items, які він створив


class ItemModel(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    # Створення зовнішнього ключа, який посилається на колонку id в таблиці users

    owner = relationship('UserModel', back_populates='items')