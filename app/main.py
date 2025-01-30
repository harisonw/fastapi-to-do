from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas

from .database import engine, get_db

app = FastAPI()


# Startup event to create database tables
@app.on_event("startup")
async def on_startup() -> None:
    """
    Initialize the database tables during application startup.

    This asynchronous function creates all database tables defined in the SQLAlchemy models
    by using the database engine's connection. It ensures that the database schema is
    set up before the application begins serving requests.

    Note:
        - Uses an asynchronous context manager to begin a database transaction
        - Runs table creation synchronously within the async context
        - Automatically creates tables if they do not already exist
    """
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


# Get all ToDo items
@app.get("/todos")
async def read_todos(db: AsyncSession = Depends(get_db)) -> list[schemas.ToDoResponse]:
    """
    Retrieve all ToDo items from the database.

    Fetches a list of all ToDo items using an asynchronous database session.

    Args:
        db (AsyncSession): An asynchronous database session dependency for database operations.

    Returns:
        list[schemas.ToDoResponse]: A list of ToDo items, each represented as a ToDoResponse schema.
    """
    return await crud.get_todos(db)


# Get a single ToDo item
@app.get("/todos/{todo_id}")
async def read_todo(
    todo_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.ToDoResponse:
    """
    Retrieve a specific ToDo item by its unique identifier.

    Fetches a single ToDo item from the database matching the provided todo_id.
    Utilizes an asynchronous database session to perform the lookup.

    Parameters:
        todo_id (int): The unique identifier of the ToDo item to retrieve
        db (AsyncSession, optional): Asynchronous database session. Defaults to dependency injection via get_db.

    Returns:
        schemas.ToDoResponse: The ToDo item corresponding to the specified todo_id

    Raises:
        HTTPException: If no ToDo item is found with the given todo_id (handled in crud.get_todo)
    """
    return await crud.get_todo(db, todo_id)  # Error handling done in crud.get_todo


# Create a new ToDo item
@app.post("/todos", status_code=201)
async def create_todo(
    todo: schemas.ToDoCreate, db: AsyncSession = Depends(get_db)
) -> schemas.ToDoResponse:
    """
    Create a new ToDo item in the database.

    This function takes a ToDoCreate schema, converts it to a database model, and persists it using the CRUD create method.

    Parameters:
        todo (schemas.ToDoCreate): The ToDo item details to be created
        db (AsyncSession, optional): Asynchronous database session. Defaults to dependency injection via get_db.

    Returns:
        schemas.ToDoResponse: The created ToDo item with database-generated fields

    Raises:
        ValidationError: If the input data does not meet Pydantic schema requirements
    """
    db_todo = models.ToDo(**todo.model_dump())  # Error handling done by Pydantic

    return await crud.create_todo(db, db_todo)


# Delete a ToDo item
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """
    Delete a specific ToDo item from the database.

    Parameters:
        todo_id (int): The unique identifier of the ToDo item to be deleted
        db (AsyncSession, optional): Asynchronous database session for performing the deletion.
            Defaults to dependency injection via get_db.

    Raises:
        HTTPException: If the ToDo item with the specified ID cannot be found or deleted
    """
    await crud.delete_todo(db, todo_id)


# Update a ToDo item
@app.put("/todos/{todo_id}")
async def update_todo(
    todo_id: int,
    todo: schemas.ToDoUpdate,
    db: AsyncSession = Depends(get_db),
) -> schemas.ToDoResponse:
    """
    Update an existing ToDo item in the database.

    Parameters:
        todo_id (int): The unique identifier of the ToDo item to be updated
        todo (schemas.ToDoUpdate): The updated information for the ToDo item
        db (AsyncSession, optional): Asynchronous database session for performing the update. Defaults to dependency injection via get_db.

    Returns:
        schemas.ToDoResponse: The updated ToDo item with its new details

    Raises:
        HTTPException: If the ToDo item cannot be found or updated
    """
    return await crud.update_todo(db, todo_id, todo)
