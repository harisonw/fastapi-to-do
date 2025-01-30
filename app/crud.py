from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import ToDo


async def create_todo(db: AsyncSession, todo: ToDo) -> ToDo:
    """
    Create a new ToDo item in the database.

    Adds the provided ToDo object to the database session, commits the transaction,
    and refreshes the object to ensure it reflects the latest database state.

    Args:
        db (AsyncSession): The asynchronous database session for performing database operations.
        todo (ToDo): The ToDo item to be created and added to the database.

    Returns:
        ToDo: The created ToDo item with any database-generated fields populated.

    Raises:
        HTTPException: A 500 Internal Server Error if the database operation fails,
                       with details about the specific error encountered during creation.

    Example:
        new_todo = ToDo(title="Buy groceries", description="Milk, eggs, bread")
        created_todo = await create_todo(async_session, new_todo)
    """
    try:
        db.add(todo)
        await db.commit()
        await db.refresh(todo)
        return todo
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating ToDo: {e}",
        ) from e


async def get_todos(db: AsyncSession) -> list[ToDo]:
    """
    Retrieve all ToDo items from the database.

    Executes an asynchronous database query to fetch all ToDo items.

    Args:
        db (AsyncSession): An active asynchronous database session.

    Returns:
        list[ToDo]: A list of all ToDo items in the database.

    Raises:
        HTTPException: A 500 server error if the database query fails,
                       with details about the underlying exception.
    """
    try:
        result = await db.execute(select(ToDo))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving ToDos: {e}",
        ) from e


async def get_todo(db: AsyncSession, todo_id: int) -> ToDo:
    """
    Retrieve a specific ToDo item by its unique identifier.

    Fetches a single ToDo item from the database matching the provided ID.
    Raises an appropriate HTTP exception if the item is not found or an error occurs during retrieval.

    Args:
        db (AsyncSession): The active database session for executing queries
        todo_id (int): The unique identifier of the ToDo item to retrieve

    Returns:
        ToDo: The ToDo item matching the specified ID

    Raises:
        HTTPException: 404 error if no ToDo item is found with the given ID
        HTTPException: 500 error for any unexpected database or server errors
    """
    try:
        result = await db.execute(select(ToDo).where(ToDo.id == todo_id))
        return result.scalar_one()
    except NoResultFound as e:
        raise HTTPException(
            status_code=404, detail=f"ToDo with ID:{todo_id} not found"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving ToDo with ID:{todo_id}: {e}",
        ) from e


async def update_todo(db: AsyncSession, todo_id: int, todo: ToDo) -> ToDo:
    """
    Update an existing ToDo item in the database.

    This function retrieves a ToDo item by its ID and updates its attributes with the provided data.
    Only non-null fields from the input are updated, preserving existing values for unspecified fields.

    Args:
        db (AsyncSession): The database session for performing the update
        todo_id (int): The unique identifier of the ToDo item to update
        todo (ToDo): The ToDo object containing updated fields

    Returns:
        ToDo: The updated ToDo item from the database

    Raises:
        HTTPException: 404 if the ToDo item is not found,
                       500 for other database or processing errors
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
        raise HTTPException(
            status_code=500,
            detail=f"Error updating ToDo: {e}",
        ) from e


async def delete_todo(db: AsyncSession, todo_id: int) -> None:
    """
    Delete a specific ToDo item from the database by its ID.

    Attempts to retrieve and delete a ToDo item using the provided database session and item ID.
    If the item is not found, a 404 HTTPException is raised by the get_todo function.
    If any other error occurs during deletion, a 500 HTTPException is raised with details.

    Args:
        db (AsyncSession): The active database session for performing the deletion.
        todo_id (int): The unique identifier of the ToDo item to be deleted.

    Raises:
        HTTPException: 404 if the ToDo item is not found,
                       500 for any other database or deletion errors.

    Example:
        await delete_todo(session, 123)  # Deletes ToDo item with ID 123
    """
    try:
        todo = await get_todo(db, todo_id)
        await db.delete(todo)
        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting ToDo: {e}",
        ) from e
