import asyncio

from repo_analyst.database.agent_run_repository import (
    AgentRunRepository,
)


async def main():

    repository = AgentRunRepository()

    run = await repository.create_run(
        question="How do webhooks work?",
        repo_path="/tmp/test",
    )

    print(run.id)


asyncio.run(main())
