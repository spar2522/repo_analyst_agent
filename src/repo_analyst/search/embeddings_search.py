from repo_analyst.search.cosine_similarity import (
    cosine_similarity,
)


class EmbeddingSearch:
    """Class for performing embedding-based searches using cosine similarity."""

    def search(
        self,
        question_embedding: list[float],
        embeddings: list,
        limit: int = 5,
    ) -> list[tuple[float, object]]:
        """
        Perform a search by comparing the question embedding to a list of embeddings.

        Args:
            question_embedding: The embedding vector representing the query.
            embeddings: A list of embedding records, each expected to have an 'embedding' attribute.
            limit: The maximum number of results to return.

        Returns:
            A list of tuples containing similarity scores and corresponding embedding records,
            sorted in descending order of similarity.
        """
        scored_items = [
            (cosine_similarity(question_embedding, embedding.embedding), embedding)
            for embedding in embeddings
        ]

        scored_items.sort(reverse=True, key=lambda x: x[0])

        return scored_items[:limit]