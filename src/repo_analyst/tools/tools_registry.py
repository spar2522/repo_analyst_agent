from repo_analyst.tools.list_files import list_files
from repo_analyst.tools.read_file import read_file
from repo_analyst.tools.search_text import search_text


"""Registry of available tools for the repo analyst.

This module defines a dictionary mapping tool names to their corresponding functions.
"""

TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "search_text": search_text,
}
"""Dictionary mapping tool names to their corresponding functions.

Each key is a string representing the tool's name, and each value is the function
that implements the tool's functionality.
"""