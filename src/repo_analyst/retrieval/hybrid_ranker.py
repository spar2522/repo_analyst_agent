from repo_analyst.database.models import FileSummary, FileEmbedding

KEYWORD_MATCHES_FOR_FULL_CONFIDENCE = 3
"""Number of keyword matches required for full confidence (1.0) in keyword scoring."""

KEYWORD_WEIGHT = 0.5
EMBEDDING_WEIGHT = 0.5
"""Weights for combining keyword and embedding scores in the final ranking."""


class HybridRanker:
    """Combines keyword and embedding scores to rank file summaries."""

    def rank(
        self,
        keyword_results: list[tuple[int, FileSummary]],
        embedding_results: list[tuple[float, FileEmbedding]],
        all_summaries: list[FileSummary],
    ) -> list[tuple[float, FileSummary]]:
        """
        Rank file summaries based on keyword and embedding scores.

        Args:
            keyword_results: List of (score, FileSummary) tuples from keyword search.
            embedding_results: List of (score, FileEmbedding) tuples from embedding search.
            all_summaries: List of all FileSummary objects for lookup.

        Returns:
            List of (final_score, FileSummary) tuples, sorted by final_score descending.
        """
        summary_lookup = {summary.file_path: summary for summary in all_summaries}

        keyword_scores = self._process_keyword_results(keyword_results)
        embedding_scores = self._process_embedding_results(embedding_results)

        merged_scores = self._merge_scores(keyword_scores, embedding_scores)
        ranked = self._create_ranked_list(merged_scores, summary_lookup)

        ranked.sort(key=lambda x: x[0], reverse=True)
        return ranked

    def _process_keyword_results(
        self, keyword_results: list[tuple[int, FileSummary]]
    ) -> dict[str, float]:
        """Normalize keyword scores to a 0-1 range."""
        keyword_scores = {}
        for score, summary in keyword_results:
            normalized_score = min(
                score / KEYWORD_MATCHES_FOR_FULL_CONFIDENCE,
                1.0,
            )
            keyword_scores[summary.file_path] = normalized_score
        return keyword_scores

    def _process_embedding_results(
        self, embedding_results: list[tuple[float, FileEmbedding]]
    ) -> dict[str, float]:
        """Extract raw embedding scores."""
        embedding_scores = {}
        for score, embedding in embedding_results:
            embedding_scores[embedding.file_path] = score
        return embedding_scores

    def _merge_scores(
        self,
        keyword_scores: dict[str, float],
        embedding_scores: dict[str, float],
    ) -> dict[str, float]:
        """Combine keyword and embedding scores using weighted sum."""
        merged_scores = {}
        all_paths = set(keyword_scores.keys()) | set(embedding_scores.keys())

        for file_path in all_paths:
            keyword_score = keyword_scores.get(file_path, 0.0)
            embedding_score = embedding_scores.get(file_path, 0.0)
            final_score = (
                KEYWORD_WEIGHT * keyword_score + EMBEDDING_WEIGHT * embedding_score
            )
            merged_scores[file_path] = final_score

        return merged_scores

    def _create_ranked_list(
        self,
        merged_scores: dict[str, float],
        summary_lookup: dict[str, FileSummary],
    ) -> list[tuple[float, FileSummary]]:
        """Generate final ranked list with summaries and scores."""
        ranked = []

        for file_path, score in merged_scores.items():
            summary = summary_lookup.get(file_path)
            if summary is None:
                continue

            ranked.append((score, summary))
            print(
                f"{file_path:<45}"
                f" Keyword={keyword_scores.get(file_path, 0.0):.2f}"
                f" Embedding={embedding_scores.get(file_path, 0.0):.2f}"
                f" Final={score:.2f}"
            )

        return ranked