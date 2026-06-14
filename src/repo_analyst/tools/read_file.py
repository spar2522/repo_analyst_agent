from pathlib import Path


def read_file(
    repo_path: str,
    file_path: str,
) -> str:
    """Read the contents of a file within a repository.

    Args:
        repo_path (str): The path to the repository root.
        file_path (str): The path to the file relative to the repository root.

    Returns:
        str: The contents of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If there are insufficient permissions to read the file.
    """
    full_path = Path(repo_path) / file_path
    return full_path.read_text()