import asyncio
import csv

from repo_analyst.database.database import AsyncSessionLocal
from repo_analyst.database.models import (
    FileSummary,
    FileEmbedding,
)


async def export_file_summaries():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            FileSummary.__table__.select().order_by(FileSummary.file_path)
        )

        rows = result.fetchall()

    with open(
        "file_summaries.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "file_path",
                "summary",
            ]
        )

        for row in rows:

            writer.writerow(
                [
                    row.file_path,
                    row.summary,
                ]
            )


async def export_embeddings():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            FileEmbedding.__table__.select().order_by(FileEmbedding.file_path)
        )

        rows = result.fetchall()

    with open(
        "file_embeddings.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "file_path",
                "dimensions",
                "first_10_values",
            ]
        )

        for row in rows:

            embedding = row.embedding

            writer.writerow(
                [
                    row.file_path,
                    len(embedding),
                    embedding[:10],
                ]
            )


async def main():

    await export_file_summaries()

    await export_embeddings()

    print("✅ Export complete.")


if __name__ == "__main__":
    asyncio.run(main())
