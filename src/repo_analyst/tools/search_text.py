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

    matches = []

    for file in list_files(repo_path):

        try:

            content = read_file(
                repo_path,
                file,
            )

            if (
                search_term.lower()
                in content.lower()
            ):

                matches.append(file)

        except Exception:

            pass

    return matches