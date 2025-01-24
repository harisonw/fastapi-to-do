from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import ToDo


async def create_todo(db: AsyncSession, todo: ToDo):
    """
    Create a new ToDo item in the database.
    
    Asynchronously adds a new ToDo item to the database, commits the transaction, and refreshes the item.
    
    Args:
        db (AsyncSession): The async database session for performing database operations.
        todo (ToDo): The ToDo item to be created and added to the database.
    
    Returns:
        ToDo: The created ToDo item, including any auto-generated fields like ID.
    
    Raises:
        HTTPException: A 500 internal server error if the database operation fails, 
                       with a detailed error message describing the specific issue.
    
    Example:
        new_todo = ToDo(title="Buy groceries", description="Milk, eggs, bread")
        created_todo = await create_todo(db_session, new_todo)
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
    Retrieve all ToDo items from the database asynchronously.
    
    Executes a database query to fetch all ToDo items using an asynchronous session.
    
    Args:
        db (AsyncSession): An active asynchronous database session.
    
    Returns:
        list: A list of all ToDo items in the database.
    
    Raises:
        HTTPException: If an error occurs during database retrieval, with a 500 status code.
    
    Example:
        todos = await get_todos(async_session)
    """
    try:
        result = await db.execute(select(ToDo))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving ToDos: {e}")


async def get_todo(db: AsyncSession, todo_id: int):
    """
    Retrieve a specific ToDo item by its unique identifier.
    
    Asynchronously fetches a single ToDo item from the database matching the provided ID.
    
    Args:
        db (AsyncSession): An active database session for executing queries
        todo_id (int): The unique identifier of the ToDo item to retrieve
    
    Returns:
        ToDo: The ToDo item corresponding to the specified ID
    
    Raises:
        HTTPException: A 500 server error if the item cannot be retrieved, 
                       with details about the specific retrieval failure
    """
    try:
        result = await db.execute(select(ToDo).where(ToDo.id == todo_id))
        todo = result.scalar_one()
        return todo
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving ToDo with ID:{todo_id}: {e}"
        )


async def update_todo(db: AsyncSession, todo_id: int, todo: ToDo):
    """
    Update an existing ToDo item in the database.
    
    Attempts to update a specific ToDo item identified by its ID with the provided data. Performs a partial update by only modifying fields that are explicitly set.
    
    Args:
        db (AsyncSession): The database session for performing the update
        todo_id (int): The unique identifier of the ToDo item to update
        todo (ToDo): The ToDo object containing updated fields
    
    Returns:
        ToDo: The updated ToDo item after successful modification
    
    Raises:
        HTTPException: A 500 error if the update fails, with details about the specific error
    """
    try:
        db_todo = await get_todo(db, todo_id)
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        await db.commit()
        return db_todo
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating ToDo: {e}")


async def delete_todo(db: AsyncSession, todo_id: int):
    """
    Delete a specific ToDo item from the database.
    
    Attempts to delete a ToDo item by its unique identifier. If the item exists, it is removed from the database and the transaction is committed.
    
    Args:
        db (AsyncSession): An active database session for performing the deletion
        todo_id (int): The unique identifier of the ToDo item to be deleted
    
    Raises:
        HTTPException: A 500 status error if deletion fails, with details about the specific error
    
    Note:
        - Requires a prior successful retrieval of the ToDo item via get_todo()
        - Performs a database transaction commit on successful deletion
        - Rolls back the transaction if any error occurs during deletion
    """
    try:
        todo = await get_todo(db, todo_id)
        if todo:
            await db.delete(todo)
            await db.commit()
        return
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting ToDo: {e}")
