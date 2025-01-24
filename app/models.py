from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean


class Base(DeclarativeBase):
    pass


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
