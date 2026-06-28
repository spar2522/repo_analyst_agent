from repo_analyst.database.models import FileSummary, FileEmbedding

KEYWORD_MATCHES_FOR_FULL_CONFIDENCE = 3

KEYWORD_WEIGHT = 0.5
EMBEDDING_WEIGHT = 0.5


class HybridRanker:

    def rank(
        self,
        keyword_results: list[tuple[int, FileSummary]],
        embedding_results: list[tuple[float, FileEmbedding]],
        all_summaries: list[FileSummary],
    ) -> list[tuple[float, FileSummary]]:

        summary_lookup = {summary.file_path: summary for summary in all_summaries}

        keyword_scores = {}

        for score, summary in keyword_results:

            keyword_scores[summary.file_path] = min(
                score / KEYWORD_MATCHES_FOR_FULL_CONFIDENCE,
                1.0,
            )

        embedding_scores = {}

        for score, embedding in embedding_results:

            embedding_scores[embedding.file_path] = score

        merged_scores = {}

        all_paths = set(keyword_scores.keys()) | set(embedding_scores.keys())

        for file_path in all_paths:

            keyword_score = keyword_scores.get(
                file_path,
                0,
            )

            embedding_score = embedding_scores.get(
                file_path,
                0,
            )

            final_score = (
                KEYWORD_WEIGHT * keyword_score + EMBEDDING_WEIGHT * embedding_score
            )

            merged_scores[file_path] = final_score

        ranked = []

        for file_path, score in merged_scores.items():

            summary = summary_lookup.get(file_path)

            if summary is None:
                continue

            ranked.append(
                (
                    score,
                    summary,
                )
            )

            print(
                f"{file_path:<45}"
                f" Keyword={keyword_scores.get(file_path, 0):.2f}"
                f" Embedding={embedding_scores.get(file_path, 0):.2f}"
                f" Final={score:.2f}"
            )

        ranked.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return ranked
