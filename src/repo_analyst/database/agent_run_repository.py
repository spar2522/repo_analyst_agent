from sqlalchemy import select

from repo_analyst.database.database import (
    AsyncSessionLocal,
)

from repo_analyst.database.models import (
    AgentRun,
)


class AgentRunRepository:
    """Repository for managing AgentRun database operations."""

    async def create_run(
        self,
        question: str,
        repo_path: str,
    ) -> AgentRun:
        """
        Create a new agent run record in the database.

        Args:
            question: The question associated with the agent run.
            repo_path: The repository path for the agent run.

        Returns:
            The created AgentRun instance.

        Raises:
            SQLAlchemyError: If there is an error during database operations.
        """
        try:
            async with AsyncSessionLocal() as db:
                run = AgentRun(
                    question=question,
                    repo_path=repo_path,
                )
                db.add(run)
                await db.commit()
                await db.refresh(run)  # Ensure the instance has generated IDs
                return run
        except Exception as e:
            # In a real application, log the error here
            raise e

    async def get_run(
        self,
        run_id: int,
    ) -> AgentRun | None:
        """
        Retrieve an agent run by its ID.

        Args:
            run_id: The ID of the agent run to retrieve.

        Returns:
            The AgentRun instance if found, otherwise None.
        """
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(AgentRun).where(AgentRun.id == run_id)
                )
                return result.scalar_one_or_none()
        except Exception as e:
            # In a real application, log the error here
            raise e