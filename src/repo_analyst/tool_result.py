from dataclasses import dataclass
from typing import Any

from repo_analyst.tool_call import ToolCall


@dataclass
class ToolResult:
    """Represents the output of a tool execution with metadata, including the
    associated tool call that generated this result.
    """

    tool_name: str  # Name of the tool that produced this result
    result: Any  # The actual result returned by the tool execution (can be of any type)
    tool_call: ToolCall  # The tool call that was used to generate this result