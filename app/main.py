from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas

from .database import engine, get_db

app = FastAPI()


# Startup event to create database tables
@app.on_event("startup")
async def on_startup():
    KEEP_EXISTING
    
    The existing docstring for the `on_startup()` function is comprehensive, clear, and follows Python docstring conventions. It provides:
    - A concise one-line summary
    - A detailed description of the function's purpose
    - Notes about the implementation details
    - Explanation of the asynchronous context and table creation process
    
    The docstring effectively communicates the function's role in database initialization and provides insights into its technical implementation. No improvements are necessary.
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


# Get all ToDo items
@app.get("/todos", response_model=list[schemas.ToDoResponse])
async def read_todos(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all ToDo items from the database.
    
    This asynchronous function fetches all existing ToDo items using the provided database session.
    
    Args:
        db (AsyncSession): An asynchronous database session for querying ToDo items.
    
    Returns:
        list: A list of all ToDo items stored in the database.
    """
    return await crud.get_todos(db)


# Get a single ToDo item
@app.get("/todos/{todo_id}", response_model=schemas.ToDoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    KEEP_EXISTING
    
    The existing docstring for the `read_todo` function is comprehensive, well-structured, and follows Python docstring conventions. It clearly explains:
    - The function's purpose
    - Parameters with their types and default behaviors
    - Return value
    - Potential exceptions
    - A note about error handling delegation
    
    The docstring provides sufficient detail for developers to understand how to use the function, its dependencies, and potential error scenarios. No improvements are necessary.
    return await crud.get_todo(db, todo_id)  # Error handling done in crud.get_todo


# Create a new ToDo item
@app.post("/todos", response_model=schemas.ToDoResponse, status_code=201)
async def create_todo(todo: schemas.ToDoCreate, db: AsyncSession = Depends(get_db)):
    KEEP_EXISTING
    
    The existing docstring for the `create_todo` function is comprehensive, well-structured, and follows Python docstring conventions. It clearly explains:
    - The function's purpose
    - Input parameters with their types and default behaviors
    - Return value
    - Potential exceptions
    - Implementation details
    
    The docstring provides sufficient context about the function's behavior, including how it converts a schema to a model and uses Pydantic for error handling. No improvements are necessary.
    db_todo = models.ToDo(**todo.model_dump())  # Error handling done by Pydantic

    return await crud.create_todo(db, db_todo)


# Delete a ToDo item
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a specific ToDo item from the database.
    
    Parameters:
        todo_id (int): The unique identifier of the ToDo item to be deleted
        db (AsyncSession): An asynchronous database session for performing the deletion
    
    Raises:
        HTTPException: If the ToDo item with the specified ID cannot be found or deleted
    """
    await crud.delete_todo(db, todo_id)


# Update a ToDo item
@app.put("/todos/{todo_id}", response_model=schemas.ToDoResponse)
async def update_todo(
    todo_id: int, todo: schemas.ToDoUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing ToDo item in the database.
    
    Parameters:
        todo_id (int): The unique identifier of the ToDo item to be updated
        todo (schemas.ToDoUpdate): The updated information for the ToDo item
        db (AsyncSession, optional): Database session for performing the update. Defaults to the session obtained from get_db dependency.
    
    Returns:
        ToDoResponse: The updated ToDo item after applying modifications
    
    Raises:
        HTTPException: If the ToDo item with the specified ID cannot be found or updated
    """
    return await crud.update_todo(db, todo_id, todo)
