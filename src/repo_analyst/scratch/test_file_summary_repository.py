import asyncio

from repo_analyst.database.file_summary_repository import (
    FileSummaryRepository,
)


async def main():

    repository = FileSummaryRepository()

    await repository.save_summary(
        repo_path="test",
        file_path="a.py",
        summary="Handles webhooks",
    )

    summary = await repository.get_summary(
        repo_path="test",
        file_path="a.py",
    )

    print(summary.summary)


asyncio.run(main())
