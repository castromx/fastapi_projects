from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from .database import Base

metadata = MetaData()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    active = Column(Boolean, default=True)

    items = relationship('ItemModel', back_populates='owner')


class ItemModel(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('UserModel', back_populates='items')
