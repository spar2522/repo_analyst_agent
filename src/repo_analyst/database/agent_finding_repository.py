from repo_analyst.database.database import (
    AsyncSessionLocal,
)

from repo_analyst.database.models import (
    AgentFinding,
)

import logging


class AgentFindingRepository:

    async def save_finding(
        self,
        run_id: int,
        file_path: str,
        finding: str,
    ) -> AgentFinding:
        """
        Save a finding to the database.

        Args:
            run_id: The ID of the agent run associated with this finding.
            file_path: The file path where the finding was detected.
            finding: The actual finding or issue detected.

        Returns:
            The saved AgentFinding record.

        Raises:
            Any exceptions raised by the database session.
        """
        try:
            async with AsyncSessionLocal() as db:
                record = AgentFinding(
                    run_id=run_id,
                    file_path=file_path,
                    finding=finding,
                )

                db.add(record)
                await db.commit()
                return record

        except Exception as e:
            logging.exception("Error saving finding to database")
            raise e