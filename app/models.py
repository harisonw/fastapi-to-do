"""Database models for the To-Do application using SQLAlchemy ORM."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy models."""

    pass


class ToDo(Base):
    """To-do item database model.

    Fields:
        id: Unique identifier for the to-do item
        title: Required title of the to-do item (max 255 chars)
        description: Optional detailed description (max 1024 chars)
        completed: Flag indicating if the item is done
        created_at: UTC timestamp of creation
        updated_at: UTC timestamp of last update
    """

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(
        String(255), CheckConstraint("length(title) > 0"), index=True, nullable=False
    )
    description = Column(String(1024), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
