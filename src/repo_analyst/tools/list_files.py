from pathlib import Path


IGNORED_DIRS = {
    # List of directories to ignore when listing files.
    # These are common development directories and caches.
    ".git",
    ".venv",
    "__pycache__",
    ".vscode",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".turbo",
    "coverage",
    ".coverage",
    ".DS_Store",
}

IGNORED_FILE_SUFFIXES = {
    # List of file suffixes to ignore when listing files.
    # These are common compiled or cache files.
    ".pyc",
    ".pyo",
    ".log",
    ".sqlite",
    ".db",
    ".lock",
}


def list_files(
    repo_path: str,
) -> list[str]:
    """List all files in the repository, excluding ignored directories and files.

    Args:
        repo_path (str): The path to the repository root.

    Returns:
        list[str]: A sorted list of relative file paths.
    """
    files = []

    root = Path(repo_path)

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(
            part.endswith(".egg-info") or part in IGNORED_DIRS
            for part in path.parts
        ):
            continue

        if path.suffix in IGNORED_FILE_SUFFIXES:
            continue

        files.append(str(path.relative_to(root)))

    return sorted(files)