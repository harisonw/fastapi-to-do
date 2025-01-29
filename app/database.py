from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./todo.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    The existing docstring is comprehensive and follows Python docstring conventions. It provides clear information about the function's purpose, usage, and includes an example. Therefore:
    
    KEEP_EXISTING
    async with SessionLocal() as session:
        yield session
