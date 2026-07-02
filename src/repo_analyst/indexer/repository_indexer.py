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

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_summary_repository = FileSummaryRepository()
        self.file_summarizer = FileSummarizer(AI())
        self.embedding_client = EmbeddingClient()
        self.file_embedding_repository = FileEmbeddingRepository()

    async def index(
        self,
        repo_path: str,
    ):
        files = list_files(repo_path=repo_path)
        indexed = 0
        skipped = 0

        for index, file_path in enumerate(files):
            self.logger.info(f"[{index + 1}/{len(files)}] {file_path}")

            try:
                existing_summary = await self.file_summary_repository.get_summary(
                    repo_path=repo_path,
                    file_path=file_path,
                )

                if existing_summary:
                    skipped += 1
                    self.logger.info(f"⚡ Already indexed file: {file_path}")
                    continue

                content = read_file(
                    repo_path=repo_path,
                    file_path=file_path,
                )

                summary = await self.file_summarizer.summarize(
                    file_path=file_path,
                    content=content,
                )

                await self.file_summary_repository.save_summary(
                    repo_path=repo_path,
                    file_path=file_path,
                    summary=summary,
                )

                indexed += 1
                self.logger.info("💾 Summary saved")

                embedding = self.embedding_client.generate_embedding(summary)
                await self.file_embedding_repository.save_embedding(
                    repo_path=repo_path,
                    file_path=file_path,
                    embedding=embedding,
                )

            except Exception as e:
                self.logger.error(f"❌ Error processing file {file_path}: {str(e)}")
                continue

        self.logger.info("")
        self.logger.info("=" * 60)
        self.logger.info("INDEX COMPLETE")
        self.logger.info("=" * 60)
        self.logger.info(f"Indexed: {indexed}")
        self.logger.info(f"Skipped: {skipped}")
