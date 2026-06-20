from dataclasses import dataclass


@dataclass
class ToolCall:
    """Represents a tool call with its associated arguments.

    Attributes:
        tool_name: Name of the tool being called (must be non-empty string)
        args: Dictionary of arguments to pass to the tool (must be a dictionary)
    """
    tool_name: str
    args: dict

    def __post_init__(self):
        """Validate tool call parameters."""
        if not isinstance(self.tool_name, str) or not self.tool_name:
            raise ValueError("tool_name must be a non-empty string")
        if not isinstance(self.args, dict):
            raise ValueError("args must be a dictionary")

    def __repr__(self):
        """Return human-readable string representation."""
        return f"ToolCall(tool_name='{self.tool_name}', args={self.args})"