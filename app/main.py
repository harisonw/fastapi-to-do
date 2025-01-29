from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas

from .database import engine, get_db

app = FastAPI()


# Startup event to create database tables
@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


# Get all ToDo items
@app.get("/todos")
async def read_todos(db: AsyncSession = Depends(get_db)) -> list[schemas.ToDoResponse]:
    return await crud.get_todos(db)


# Get a single ToDo item
@app.get("/todos/{todo_id}")
async def read_todo(
    todo_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.ToDoResponse:
    return await crud.get_todo(db, todo_id)  # Error handling done in crud.get_todo


# Create a new ToDo item
@app.post("/todos", status_code=201)
async def create_todo(
    todo: schemas.ToDoCreate, db: AsyncSession = Depends(get_db)
) -> schemas.ToDoResponse:
    db_todo = models.ToDo(**todo.model_dump())  # Error handling done by Pydantic

    return await crud.create_todo(db, db_todo)


# Delete a ToDo item
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)) -> None:
    await crud.delete_todo(db, todo_id)


# Update a ToDo item
@app.put("/todos/{todo_id}")
async def update_todo(
    todo_id: int,
    todo: schemas.ToDoUpdate,
    db: AsyncSession = Depends(get_db),
) -> schemas.ToDoResponse:
    return await crud.update_todo(db, todo_id, todo)
