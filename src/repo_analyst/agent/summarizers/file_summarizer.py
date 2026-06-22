def summarize_file(
    file_path: str,
    content: str,
) -> str:
    """
    Generate a summary of the provided file content.

    Args:
        file_path: Path to the file being summarized.
        content: Full text content of the file.

    Returns:
        A string summary indicating the number of lines in the file.
    """
    return f"File {file_path} contains {len(content.splitlines())} lines."