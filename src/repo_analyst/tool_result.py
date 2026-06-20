from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    """Represents the output of a tool execution with metadata."""

    tool_name: str  # Name of the tool that produced this result
    result: Any  # The actual result returned by the tool execution