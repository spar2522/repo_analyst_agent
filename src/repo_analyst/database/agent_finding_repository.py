from repo_analyst.database.database import (
    AsyncSessionLocal,
)

from repo_analyst.database.models import (
    AgentFinding,
)


class AgentFindingRepository:

    async def save_finding(
        self,
        run_id: int,
        file_path: str,
        finding: str,
    ):

        async with AsyncSessionLocal() as db:

            record = AgentFinding(
                run_id=run_id,
                file_path=file_path,
                finding=finding,
            )

            db.add(record)

            await db.commit()
