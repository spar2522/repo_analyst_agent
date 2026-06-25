"""Test script for FileSummaryRepository.

This script demonstrates saving and retrieving file summaries using the FileSummaryRepository.
"""

import asyncio

from repo_analyst.database.file_summary_repository import (
    FileSummaryRepository,
)


async def main() -> None:
    """Main function to test FileSummaryRepository.

    Saves a summary for a test file and retrieves it to verify functionality.
    """
    repository: FileSummaryRepository = FileSummaryRepository()

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