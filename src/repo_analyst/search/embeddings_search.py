from repo_analyst.search.cosine_similarity import (
    cosine_similarity,
)


class EmbeddingSearch:

    def search(
        self,
        question_embedding: list[float],
        embeddings: list,
        limit: int = 5,
    ):

        scored = []

        for embedding_record in embeddings:

            score = cosine_similarity(
                question_embedding,
                embedding_record.embedding,
            )

            scored.append(
                (
                    score,
                    embedding_record,
                )
            )

        scored.sort(
            reverse=True,
            key=lambda x: x[0],
        )

        return scored[:limit]
