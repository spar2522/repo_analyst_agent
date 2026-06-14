from pathlib import Path


IGNORED_DIRS = {
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

    files = []

    root = Path(repo_path)

    for file in root.rglob("*"):

        if not file.is_file():
            continue

        if any(
            part.endswith(".egg-info")
            or part in IGNORED_DIRS
            for part in file.parts
        ):
            continue

        if file.suffix in IGNORED_FILE_SUFFIXES:
            continue

        files.append(
            str(
                file.relative_to(root)
            )
        )

    return sorted(files)