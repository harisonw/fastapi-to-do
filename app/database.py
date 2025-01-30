import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo.db")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

engine = create_async_engine(DATABASE_URL, echo=DEBUG)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session generator for database interactions.

    This generator creates and manages a new database session for each request,
    ensuring proper resource allocation and cleanup in asynchronous database operations.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy database session that can be used
                      for database queries and transactions.

    Note:
        - The session is automatically closed after use due to the async context manager.
        - Recommended for use with FastAPI dependency injection.
    """
    async with SessionLocal() as session:
        yield session
