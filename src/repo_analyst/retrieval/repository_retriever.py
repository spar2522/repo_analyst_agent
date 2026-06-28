from repo_analyst.database.file_summary_repository import (
    FileSummaryRepository,
)
from repo_analyst.database.file_embedding_repository import (
    FileEmbeddingRepository,
)

from repo_analyst.search.summary_search import (
    SummarySearch,
)

from repo_analyst.search.embeddings_search import (
    EmbeddingSearch,
)

from repo_analyst.llm.embeddings_client import (
    EmbeddingClient,
)

from repo_analyst.retrieval.hybrid_ranker import HybridRanker


class RepositoryRetriever:

    def __init__(self):

        self.summary_repository = FileSummaryRepository()

        self.embedding_repository = FileEmbeddingRepository()

        self.summary_search = SummarySearch()

        self.embedding_search = EmbeddingSearch()

        self.embedding_client = EmbeddingClient()

        self.hybrid_ranker = HybridRanker()

    async def retrieve(
        self,
        repo_path: str,
        question: str,
    ):
        summaries = await self.summary_repository.get_all_summaries(repo_path)
        keyword_results = await self.summary_search.search(
            question=question,
            summaries=summaries,
        )
        embeddings = await self.embedding_repository.get_all_embeddings(repo_path)
        question_embedding = self.embedding_client.generate_embedding(question)
        embedding_results = self.embedding_search.search(
            question_embedding=question_embedding,
            embeddings=embeddings,
        )

        print()

        print("Keyword Search")

        for score, summary in keyword_results:

            print(
                score,
                summary.file_path,
            )

        print()

        print("Embedding Search")

        for score, embedding in embedding_results:

            print(
                f"{score:.3f}",
                embedding.file_path,
            )

        return self.hybrid_ranker.rank(keyword_results, embedding_results, summaries)
