from dataclasses import dataclass
from typing import Any

from repo_analyst.tool_call import ToolCall


@dataclass
class ToolResult:
    """Represents the output of a tool execution with metadata."""

    tool_name: str  # Name of the tool that produced this result

    result: Any  # The actual result returned by the tool execution

    tool_call: ToolCall
