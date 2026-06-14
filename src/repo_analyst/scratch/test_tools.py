from repo_analyst.tools.list_files import (
    list_files,
)

from repo_analyst.tools.search_text import (
    search_text,
)
from repo_analyst.tools.tools_registry import TOOLS

REPO = (
    "/Users/arpitratan/ai-lab/ai_autodoc"
)

files = list_files(REPO)

print(
    f"Found {len(files)} files"
)

matches = search_text(
    REPO,
    "redis",
)

print()

print(
    "Files mentioning redis:"
)

for match in matches:

    print(match)

tool_name = "list_files"

result = TOOLS[tool_name](
    repo_path="."
)

print(result[:5])