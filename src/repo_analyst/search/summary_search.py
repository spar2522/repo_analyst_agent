from repo_analyst.database.models import FileSummary


class SummarySearch:

    async def search(
        self,
        question: str,
        summaries: list,
    ) -> list[tuple[int, FileSummary]]:

        question_words = set(question.lower().split())

        scored = []

        for summary in summaries:

            summary_words = set(summary.summary.lower().split())

            score = len(question_words & summary_words)

            scored.append(
                (
                    score,
                    summary,
                )
            )

        scored.sort(reverse=True, key=lambda x: x[0])

        return scored[:5]
