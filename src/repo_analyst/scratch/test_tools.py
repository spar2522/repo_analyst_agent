from repo_analyst.tools.list_files import (
    list_files,
)

from repo_analyst.tools.search_text import (
    search_text,
)
from repo_analyst.tools.tools_registry import TOOLS

# Configuration: Repository path to analyze
REPO = "/Users/arpitratan/ai-lab/ai_autodoc"

# List all files in the repository
files = list_files(REPO)

# Output the number of files found
print(f"Found {len(files)} files")

# Search for files containing the term "redis"
matches = search_text(REPO, "redis")

# Output the results of the search
print()
print("Files mentioning redis:")
for match in matches:
    print(match)

# Example usage of the tools registry
tool_name = "list_files"
result = TOOLS[tool_name](repo_path=".")

# Output the first 5 results from the tool
print(result[:5])