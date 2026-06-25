from sqlalchemy import select
from repo_analyst.database.database import AsyncSessionLocal
from repo_analyst.database.models import FileEmbedding


class FileEmbeddingRepository:
    """Repository for managing file embeddings in the database."""

    async def save_embedding(
        self,
        repo_path: str,
        file_path: str,
        embedding: list[float],
    ) -> None:
        """Save a file's embedding to the database.

        Args:
            repo_path: Path to the repository.
            file_path: Path to the file within the repository.
            embedding: The embedding vector as a list of floats.
        """
        try:
            async with AsyncSessionLocal() as db:
                record = FileEmbedding(
                    repo_path=repo_path,
                    file_path=file_path,
                    embedding=embedding,
                )
                db.add(record)
                await db.commit()
        except Exception as e:
            # Log the error and re-raise to ensure caller is aware of failure
            # (logging implementation would be added in production)
            raise e

    async def get_all_embeddings(
        self,
        repo_path: str,
    ) -> list[FileEmbedding]:
        """Retrieve all embeddings for a given repository path.

        Args:
            repo_path: Path to the repository.

        Returns:
            List of FileEmbedding records for the specified repository.
        """
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(FileEmbedding).where(FileEmbedding.repo_path == repo_path)
            )
            return result.scalars().all()