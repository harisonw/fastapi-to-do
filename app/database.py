from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./todo.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """
    Asynchronous database session generator for dependency injection.
    
    This generator creates and manages an asynchronous SQLAlchemy database session, 
    which can be used for database operations within an async context.
    
    Yields:
        AsyncSession: An asynchronous database session that can be used for database queries and transactions.
    
    Note:
        - The session is automatically closed after use due to the async context manager.
        - Intended to be used with FastAPI's dependency injection system.
    
    Example:
        async def some_endpoint(db: AsyncSession = Depends(get_db)):
            # Use db for database operations
            result = await db.execute(some_query)
    """
    async with SessionLocal() as session:
        yield session
