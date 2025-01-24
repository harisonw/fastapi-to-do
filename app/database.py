from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./todo.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """
    Asynchronous database session generator for SQLAlchemy database interactions.
    
    This generator function creates and manages an asynchronous database session that can be used in database operations.
    
    Yields:
        AsyncSession: An asynchronous SQLAlchemy database session that will be automatically closed after use.
    
    Usage:
        Typically used with FastAPI dependency injection to provide database sessions to route handlers.
    """
    async with SessionLocal() as session:
        yield session
