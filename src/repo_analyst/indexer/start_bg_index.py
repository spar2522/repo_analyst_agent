import asyncio
import logging

from repo_analyst.indexer.repository_indexer import (
    RepositoryIndexer,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"


async def main():

    indexer = RepositoryIndexer()

    await indexer.index(
        repo_path=REPO_PATH,
    )


asyncio.run(main())
