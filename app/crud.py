from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import ToDo


async def create_todo(db: AsyncSession, todo: ToDo):
    try:
        db.add(todo)
        await db.commit()
        await db.refresh(todo)
        return todo
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating ToDo: {e}")


async def get_todos(db: AsyncSession):
    try:
        result = await db.execute(select(ToDo))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving ToDos: {e}")


async def get_todo(db: AsyncSession, todo_id: int):
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
    try:
        todo = await get_todo(db, todo_id)
        await db.delete(todo)
        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting ToDo: {e}")
