from repo_analyst.database.database import (
    engine,
    Base,
)

import asyncio


async def init_db():
    """Initialize the database by creating all tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Database initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise


asyncio.run(init_db())