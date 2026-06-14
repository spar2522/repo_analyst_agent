from pathlib import Path


def read_file(
    repo_path: str,
    file_path: str,
) -> str:

    full_path = (
        Path(repo_path)
        / file_path
    )

    return full_path.read_text()