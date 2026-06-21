def extract_search_term(
    question: str,
) -> str:

    question = question.lower()

    if "redis" in question:
        return "redis"

    if "webhook" in question:
        return "webhook"

    if "github" in question:
        return "github"

    return question
