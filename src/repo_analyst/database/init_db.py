from repo_analyst.database.database import (
    engine,
    Base,
)

from repo_analyst.database.models import AgentRun

import asyncio


async def init_db():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

        print("Database initialized successfully.")


asyncio.run(init_db())
