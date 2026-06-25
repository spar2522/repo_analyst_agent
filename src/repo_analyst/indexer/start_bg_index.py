import asyncio
import logging
import os

from repo_analyst.indexer.repository_indexer import RepositoryIndexer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

REPO_PATH = os.environ.get("REPO_PATH", "/Users/arpitratan/ai-lab/ai_autodoc")


async def main():
    """
    Entry point for background indexing process.

    Initializes RepositoryIndexer and triggers indexing operation
    on specified repository path.
    """
    try:
        indexer = RepositoryIndexer()
        await indexer.index(repo_path=REPO_PATH)
    except Exception as e:
        logging.error("Indexing failed: %s", e, exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())