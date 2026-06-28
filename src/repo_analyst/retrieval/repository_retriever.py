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
    """A class to retrieve relevant files from a repository based on a question."""

    def __init__(self):
        """Initialize the RepositoryRetriever with required components."""
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
        """Retrieve relevant files from the repository based on the given question.

        Args:
            repo_path: The path to the repository.
            question: The question to search for.

        Returns:
            The ranked results from the hybrid ranker.
        """
        try:
            # Fetch summaries from the repository
            summaries = await self.summary_repository.get_all_summaries(repo_path)
            if not summaries:
                print("No summaries found in the repository.")
                return []

            # Search for relevant summaries
            keyword_results = await self.summary_search.search(summaries, question)

            # Fetch embeddings from the repository
            embeddings = await self.embedding_repository.get_all_embeddings(repo_path)
            if not embeddings:
                print("No embeddings found in the repository.")
                return []

            # Generate embedding for the question
            try:
                question_embedding = await self.embedding_client.generate_embedding(question)
            except Exception as e:
                print(f"Failed to generate embedding for the question: {e}")
                return []

            # Search for relevant embeddings
            try:
                embedding_results = await self.embedding_search.search(embeddings, question_embedding)
            except Exception as e:
                print(f"Failed to search embeddings: {e}")
                return []

            # Combine results using hybrid ranker
            ranked_results = self.hybrid_ranker.rank(keyword_results, embedding_results, summaries)

            # Output results
            print("Retrieved results:")
            for result in ranked_results:
                print(f"- {result.file_path}")

            return ranked_results

        except Exception as e:
            print(f"An error occurred during retrieval: {e}")
            return []