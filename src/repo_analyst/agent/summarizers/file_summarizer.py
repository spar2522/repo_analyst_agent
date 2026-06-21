def summarize_file(
    file_path: str,
    content: str,
) -> str:

    return f"File {file_path} contains " f"{len(content.splitlines())} lines."
