from sqlalchemy import select

from repo_analyst.database.database import (
    AsyncSessionLocal,
)

from repo_analyst.database.models import (
    FileSummary,
)


class FileSummaryRepository:

    async def save_summary(
        self,
        repo_path: str,
        file_path: str,
        summary: str,
    ):

        async with AsyncSessionLocal() as db:

            record = FileSummary(
                repo_path=repo_path,
                file_path=file_path,
                summary=summary,
            )

            db.add(record)

            await db.commit()

    async def get_summary(
        self,
        repo_path: str,
        file_path: str,
    ):

        async with AsyncSessionLocal() as db:

            result = await db.execute(
                select(FileSummary)
                .where(
                    FileSummary.repo_path == repo_path,
                )
                .where(
                    FileSummary.file_path == file_path,
                )
            )

            return result.scalars().first()
