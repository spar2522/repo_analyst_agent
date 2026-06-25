from repo_analyst.database.models import FileSummary


class SummarySearch:
    """Class for searching file summaries based on keyword matching."""

    async def search(
        self,
        question: str,
        summaries: list[FileSummary],
    ) -> list[tuple[int, FileSummary]]:
        """
        Search summaries for relevance to the given question.

        Args:
            question: The query string to search for.
            summaries: List of FileSummary objects to search through.

        Returns:
            List of tuples containing (score, FileSummary), sorted by score descending.
            Only the top 5 results are returned.

        Notes:
            - Scoring is based on the number of unique words matching between
              the question and summary (case-insensitive).
            - Basic whitespace splitting is used for tokenization.
            - Summary text is assumed to be non-null.
        """
        # Convert question to lowercase and split into words
        question_words = set(question.lower().split())

        scored_summaries = []

        for summary in summaries:
            # Skip if summary text is missing
            if not summary.summary:
                continue

            # Convert summary to lowercase and split into words
            summary_words = set(summary.summary.lower().split())

            # Calculate intersection count as score
            score = len(question_words & summary_words)

            scored_summaries.append((score, summary))

        # Sort by score descending and return top 5 results
        scored_summaries.sort(reverse=True, key=lambda x: x[0])
        return scored_summaries[:5]