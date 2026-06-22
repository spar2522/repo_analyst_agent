import asyncio

from repo_analyst.database.agent_run_repository import (
    AgentRunRepository,
)


async def main():
    """Test the creation of an agent run."""
    try:
        repository = AgentRunRepository()
        run = await repository.create_run(
            question="How do webhooks work?",
            repo_path="/tmp/test",
        )
        print(f"Created run with ID: {run.id}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


asyncio.run(main())