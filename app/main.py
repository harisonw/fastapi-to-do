from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas

from .database import engine, get_db

app = FastAPI()


# Startup event to create database tables
@app.on_event("startup")
async def on_startup():
    """
    Initialize the database by creating all defined database tables during application startup.
    
    This asynchronous function uses SQLAlchemy's metadata to create database tables synchronously within an asynchronous database connection context. It ensures that all database models defined in the application are properly set up before the application begins serving requests.
    
    Note:
        - This function is typically registered as a startup event handler in FastAPI
        - It uses an asynchronous connection to begin a transaction and create tables
        - Tables are created based on the metadata defined in the SQLAlchemy models
    """
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
    
    Raises:
        Any database-related exceptions will be propagated from the underlying CRUD operation.
    """
    return await crud.get_todos(db)


# Get a single ToDo item
@app.get("/todos/{todo_id}", response_model=schemas.ToDoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific ToDo item by its unique identifier.
    
    Fetches a single ToDo item from the database using the provided todo_id. 
    Error handling for non-existent items is managed within the crud.get_todo method.
    
    Args:
        todo_id (int): The unique identifier of the ToDo item to retrieve
        db (AsyncSession): Asynchronous database session for performing the query
    
    Returns:
        models.ToDo: The ToDo item corresponding to the given todo_id
    
    Raises:
        HTTPException: If the ToDo item cannot be found (handled in crud.get_todo)
    """
    return await crud.get_todo(db, todo_id)  # Error handling done in crud.get_todo


# Create a new ToDo item
@app.post("/todos", response_model=schemas.ToDoResponse, status_code=201)
async def create_todo(todo: schemas.ToDoCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new ToDo item in the database.
    
    Validates the input ToDo item using Pydantic schema and creates a database record.
    
    Args:
        todo (schemas.ToDoCreate): The ToDo item details to be created
        db (AsyncSession, optional): Database session for transaction. Defaults to dependency injection via get_db.
    
    Returns:
        models.ToDo: The newly created ToDo item with assigned database ID
    
    Raises:
        ValueError: If the input data fails Pydantic validation
        SQLAlchemyError: If there's an issue with database transaction
    """
    db_todo = models.ToDo(**todo.model_dump())  # Error handling done by Pydantic

    return await crud.create_todo(db, db_todo)


# Delete a ToDo item
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a specific ToDo item from the database.
    
    Deletes the ToDo item with the given ID using the provided database session.
    
    Args:
        todo_id (int): The unique identifier of the ToDo item to be deleted
        db (AsyncSession): Asynchronous database session for performing the deletion
    
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
        todo (schemas.ToDoUpdate): The updated ToDo item data
        db (AsyncSession, optional): Database session for performing the update. Defaults to dependency-injected session.
    
    Returns:
        models.ToDo: The updated ToDo item from the database
    
    Raises:
        HTTPException: If the ToDo item cannot be found or updated
    """
    return await crud.update_todo(db, todo_id, todo)
