def extract_search_term(
    question: str,
) -> str:
    """
    Extracts a specific search term from the given question.

    The function checks for the presence of predefined keywords in the question
    (case-insensitively) and returns the corresponding keyword if found. If no
    keyword is found, the entire question is returned in lowercase.

    Args:
        question: The input question string.

    Returns:
        A specific keyword if found, otherwise the lowercase version of the question.
    """
    question = question.lower()

    # Map of keywords to return values. Order matters; the first match is used.
    KEYWORD_MAP = [
        ("redis", "redis"),
        ("webhook", "webhook"),
        ("github", "github"),
    ]

    for keyword, value in KEYWORD_MAP:
        if keyword in question:
            return value

    return question