from sqlalchemy import select, and_

from repo_analyst.database.database import AsyncSessionLocal
from repo_analyst.database.models import FileSummary


class FileSummaryRepository:
    """Repository for managing file summaries in the database."""

    async def save_summary(
        self,
        repo_path: str,
        file_path: str,
        summary: str,
    ) -> None:
        """Saves a file summary to the database.

        Args:
            repo_path (str): The path to the repository.
            file_path (str): The path to the file within the repository.
            summary (str): The summary of the file content.

        Raises:
            SQLAlchemyError: If there's an error during the database operation.
        """
        try:
            async with AsyncSessionLocal() as db:
                record = FileSummary(
                    repo_path=repo_path,
                    file_path=file_path,
                    summary=summary,
                )
                db.add(record)
                await db.commit()
        except Exception as e:
            raise e

    async def get_summary(
        self,
        repo_path: str,
        file_path: str,
    ) -> FileSummary | None:
        """Retrieves a file summary by repository and file path.

        Args:
            repo_path (str): The path to the repository.
            file_path (str): The path to the file within the repository.

        Returns:
            FileSummary | None: The file summary if found, otherwise None.
        """
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(FileSummary)
                .where(
                    and_(
                        FileSummary.repo_path == repo_path,
                        FileSummary.file_path == file_path,
                    )
                )
            )
            return result.scalars().first()

    async def get_all_summaries(
        self,
        repo_path: str,
    ) -> list[FileSummary]:
        """Retrieves all file summaries for a given repository.

        Args:
            repo_path (str): The path to the repository.

        Returns:
            list[FileSummary]: A list of all file summaries for the repository.
        """
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(FileSummary).where(FileSummary.repo_path == repo_path)
            )
        return list(result.scalars().all())