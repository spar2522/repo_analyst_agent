from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:

    tool_name: str

    result: Any
