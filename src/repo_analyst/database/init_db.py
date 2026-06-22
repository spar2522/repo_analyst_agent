from repo_analyst.database.database import (
    engine,
    Base,
)

import asyncio


async def init_db():
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Database initialized successfully.")


asyncio.run(init_db())