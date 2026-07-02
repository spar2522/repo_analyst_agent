import logging

from repo_analyst.database.file_summary_repository import (
    FileSummaryRepository,
)
from repo_analyst.database.file_embedding_repository import (
    FileEmbeddingRepository,
)
from repo_analyst.tools.list_files import list_files
from repo_analyst.tools.read_file import read_file
from repo_analyst.llm.file_summariser import (
    FileSummarizer,
)
from ai_provider import AI

from repo_analyst.llm.embeddings_client import (
    EmbeddingClient,
)


class RepositoryIndexer:
    """Indexes a repository by generating file summaries and embeddings."""

    def __init__(self):
        """Initialize the RepositoryIndexer with required components."""
        self.logger = logging.getLogger(__name__)
        self.file_summary_repository = FileSummaryRepository()
        self.file_summarizer = FileSummarizer(AI())
        self.embedding_client = EmbeddingClient()
        self.file_embedding_repository = FileEmbeddingRepository()

    async def index(
        self,
        repo_path: str,
    ) -> None:
        """Index all files in the specified repository.

        Args:
            repo_path: Path to the repository to be indexed.
        """
        files = list_files(repo_path=repo_path)
        indexed = 0
        skipped = 0

        for index, file_path in enumerate(files):
            self.logger.info(f"[{index + 1}/{len(files)}] {file_path}")

            try:
                if await self._is_file_already_indexed(file_path):
                    skipped += 1
                    self.logger.info(f"⚡ Already indexed file: {file_path}")
                    continue

                content = read_file(repo_path=repo_path, file_path=file_path)
                summary = await self.file_summarizer.summarize(
                    file_path=file_path,
                    content=content,
                )

                await self._save_summary_and_embedding(file_path, summary)
                indexed += 1
                self.logger.info("💾 Summary saved")

            except Exception as e:
                self.logger.error(f"❌ Error processing file {file_path}: {str(e)}")
                continue

        self.logger.info("=" * 60)
        self.logger.info("INDEX COMPLETE")
        self.logger.info("=" * 60)
        self.logger.info(f"Indexed: {indexed}")
        self.logger.info(f"Skipped: {skipped}")

    async def _is_file_already_indexed(self, file_path: str) -> bool:
        """Check if a file has already been indexed.

        Args:
            file_path: Path to the file being checked.

        Returns:
            True if the file is already indexed, False otherwise.
        """
        existing_summary = await self.file_summary_repository.get_summary(
            repo_path=repo_path,
            file_path=file_path,
        )
        return existing_summary is not None

    async def _save_summary_and_embedding(
        self,
        file_path: str,
        summary: str,
    ) -> None:
        """Save the summary and embedding for a file.

        Args:
            file_path: Path to the file.
            summary: Summary of the file content.
        """
        await self.file_summary_repository.save_summary(
            repo_path=repo_path,
            file_path=file_path,
            summary=summary,
        )

        embedding = self.embedding_client.generate_embedding(summary)
        await self.file_embedding_repository.save_embedding(
            repo_path=repo_path,
            file_path=file_path,
            embedding=embedding,
        )