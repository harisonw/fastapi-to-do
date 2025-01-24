from typing import Optional

from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(ToDoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class ToDoResponse(ToDoBase):
    id: int

    class Config:
        from_attributes = True  # Allows compatibility with SQLAlchemy models
