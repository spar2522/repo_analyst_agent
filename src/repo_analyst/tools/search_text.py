from pathlib import Path

from repo_analyst.tools.list_files import (
    list_files,
)

from repo_analyst.tools.read_file import (
    read_file,
)


def search_text(
    repo_path: str,
    search_term: str,
) -> list[str]:
    """Search for a text term in all files within a repository.

    Args:
        repo_path (str): Path to the repository root.
        search_term (str): Text term to search for (case-insensitive).

    Returns:
        list[str]: List of file paths containing the search term.

    Examples:
        >>> search_text('/path/to/repo', 'function')
        ['/path/to/repo/file1.py', '/path/to/repo/file2.py']
    """
    matches = []

    for file_path in list_files(repo_path):

        try:

            content = read_file(
                repo_path,
                file_path,
            )

            if search_term.lower() in content.lower():

                matches.append(file_path)

        except Exception:

            pass

    return matches