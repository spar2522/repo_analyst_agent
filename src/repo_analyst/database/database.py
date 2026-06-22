from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()
DATABASE_URL = "postgresql+asyncpg://admin:password@localhost:5432/repo_analyst"

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
)


async def get_async_db():
    """Asynchronous context manager to yield an async database session.

    Yields:
        AsyncSession: An async SQLAlchemy session for database operations.
    """
    async with AsyncSessionLocal() as db:
        yield db