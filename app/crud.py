from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import ToDo


async def create_todo(db: AsyncSession, todo: ToDo):
    """
    Create a new ToDo item in the database.
    
    Adds the provided ToDo object to the database session, commits the transaction,
    and refreshes the object to reflect its database-assigned state.
    
    Args:
        db (AsyncSession): The async database session for performing database operations.
        todo (ToDo): The ToDo object to be created and stored in the database.
    
    Returns:
        ToDo: The created ToDo object with updated database-assigned attributes.
    
    Raises:
        HTTPException: A 500 Internal Server Error if the database operation fails,
                       with details about the specific error encountered.
    
    Example:
        todo = ToDo(title="Buy groceries", description="Milk, eggs, bread")
        created_todo = await create_todo(db_session, todo)
    """
    try:
        db.add(todo)
        await db.commit()
        await db.refresh(todo)
        return todo
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating ToDo: {e}")


async def get_todos(db: AsyncSession):
    """
    Retrieve all ToDo items from the database.
    
    Executes an asynchronous database query to fetch all ToDo objects.
    
    Args:
        db (AsyncSession): An active database session for executing queries.
    
    Returns:
        list[ToDo]: A list of all ToDo objects in the database.
    
    Raises:
        HTTPException: If an error occurs during database retrieval, with a 500 status code.
    """
    try:
        result = await db.execute(select(ToDo))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving ToDos: {e}")


async def get_todo(db: AsyncSession, todo_id: int):
    """
    Retrieve a specific ToDo item by its unique identifier.
    
    Asynchronously fetches a single ToDo object from the database matching the provided ID.
    
    Args:
        db (AsyncSession): Active database session for executing queries
        todo_id (int): Unique identifier of the ToDo item to retrieve
    
    Returns:
        ToDo: The ToDo object corresponding to the specified ID
    
    Raises:
        HTTPException: 404 error if no ToDo is found with the given ID
        HTTPException: 500 error for unexpected database or query errors
    """
    try:
        result = await db.execute(select(ToDo).where(ToDo.id == todo_id))
        todo = result.scalar_one()
        return todo
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"ToDo with ID:{todo_id} not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving ToDo with ID:{todo_id}: {e}"
        )


async def update_todo(db: AsyncSession, todo_id: int, todo: ToDo):
    """
    Update an existing ToDo item in the database.
    
    This asynchronous function updates a specific ToDo item identified by its ID with the provided data. It selectively updates only the fields that are explicitly set in the input.
    
    Args:
        db (AsyncSession): The database session for performing the update operation.
        todo_id (int): The unique identifier of the ToDo item to be updated.
        todo (ToDo): The ToDo object containing the updated fields.
    
    Returns:
        ToDo: The updated ToDo object with modified attributes.
    
    Raises:
        HTTPException: 404 if the ToDo item is not found, or 500 for other database-related errors.
    
    Example:
        updated_todo = await update_todo(session, 1, ToDo(title="New Title"))
    """
    try:
        db_todo = await get_todo(db, todo_id)
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        await db.commit()
        return db_todo
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating ToDo: {e}")


async def delete_todo(db: AsyncSession, todo_id: int):
    """
    Delete a specific ToDo item from the database.
    
    Attempts to delete a ToDo item with the given ID. First retrieves the item using get_todo,
    then removes it from the database. Handles potential errors by rolling back the transaction
    and raising an appropriate HTTP exception.
    
    Args:
        db (AsyncSession): The database session for performing the deletion
        todo_id (int): The unique identifier of the ToDo item to be deleted
    
    Raises:
        HTTPException: 404 if the ToDo item is not found (via get_todo)
        HTTPException: 500 if an unexpected error occurs during deletion
    
    Example:
        await delete_todo(session, 123)  # Deletes ToDo with ID 123
    """
    try:
        todo = await get_todo(db, todo_id)
        await db.delete(todo)
        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting ToDo: {e}")
