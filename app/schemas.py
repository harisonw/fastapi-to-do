"""Pydantic models for request/response data validation."""

from typing import Optional

from pydantic import BaseModel


class ToDoBase(BaseModel):
    """Base Pydantic model for To-Do items.
    
    Attributes:
        title: The title of the to-do item
        description: Optional detailed description
        completed: Whether the item is completed
    """
    title: str
    description: str | None = None
    completed: bool = False


class ToDoCreate(ToDoBase):
    """Schema for creating a new To-Do item."""
    pass


class ToDoUpdate(ToDoBase):
    """Schema for updating an existing To-Do item.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        title: Optional updated title
        description: Optional updated description
        completed: Optional updated completion status
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class ToDoResponse(ToDoBase):
    """Schema for To-Do item responses.
    
    Extends ToDoBase with database id.
    
    Attributes:
        id: Unique identifier from the database
    """
    id: int

    class Config:
        from_attributes = True  # Allows compatibility with SQLAlchemy models
