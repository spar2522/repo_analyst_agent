from sqlalchemy import select

from repo_analyst.database.database import (
    AsyncSessionLocal,
)

from repo_analyst.database.models import (
    FileEmbedding,
)


class FileEmbeddingRepository:

    async def save_embedding(
        self,
        repo_path: str,
        file_path: str,
        embedding: list[float],
    ):

        async with AsyncSessionLocal() as db:

            record = FileEmbedding(
                repo_path=repo_path,
                file_path=file_path,
                embedding=embedding,
            )

            db.add(record)

            await db.commit()

    async def get_all_embeddings(
        self,
        repo_path: str,
    ):

        async with AsyncSessionLocal() as db:

            result = await db.execute(
                select(FileEmbedding).where(FileEmbedding.repo_path == repo_path)
            )

            return result.scalars().all()
