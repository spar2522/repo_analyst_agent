from pydantic import BaseModel


class ToolCall(BaseModel):
    tool: str
    args: dict