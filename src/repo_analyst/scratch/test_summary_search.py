import asyncio

from repo_analyst.database.file_summary_repository import (
    FileSummaryRepository,
)
from repo_analyst.search.summary_search import SummarySearch

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"


async def main():

    repository = FileSummaryRepository()

    summaries = await repository.get_all_summaries(REPO_PATH)

    search = SummarySearch()

    results = search.search(
        question="How are webhooks processed?",
        summaries=summaries,
    )


import asyncio

from repo_analyst.database.file_summary_repository import (
    FileSummaryRepository,
)
from repo_analyst.search.summary_search import SummarySearch

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"


async def main():

    repository = FileSummaryRepository()

    summaries = await repository.get_all_summaries(REPO_PATH)

    search = SummarySearch()

    results = search.search(
        question="How are webhooks processed?",
        summaries=summaries,
    )

    for score, summary in results:
        print(f"{score:3} | {summary.file_path}")


asyncio.run(main())
