from sqlalchemy import select

from repo_analyst.database.database import (
    AsyncSessionLocal,
)

from repo_analyst.database.models import (
    AgentRun,
)


class AgentRunRepository:

    async def create_run(
        self,
        question: str,
        repo_path: str,
    ) -> AgentRun:

        async with AsyncSessionLocal() as db:

            run = AgentRun(
                question=question,
                repo_path=repo_path,
            )

            db.add(run)

            await db.commit()

            await db.refresh(run)

            return run

    async def get_run(
        self,
        run_id: int,
    ) -> AgentRun | None:

        async with AsyncSessionLocal() as db:

            result = await db.execute(select(AgentRun).where(AgentRun.id == run_id))

            return result.scalar_one_or_none()
