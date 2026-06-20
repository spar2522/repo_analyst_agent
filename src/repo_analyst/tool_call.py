from dataclasses import dataclass


@dataclass
class ToolCall:
    tool_name: str
    args: dict
