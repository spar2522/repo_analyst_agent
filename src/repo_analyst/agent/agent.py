from repo_analyst.agent.agent_state import AgentState
from repo_analyst.tool_call import ToolCall
from repo_analyst.tools.tools_registry import TOOLS
from repo_analyst.tool_result import ToolResult


class Agent:
    """Main agent class that coordinates tool execution and state management."""

    def __init__(self, state: AgentState):
        """
        Initialize the agent with a state object.

        Args:
            state: AgentState object containing the agent's current state
        """
        self.state = state

    def execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """
        Execute a tool call and return the result.

        Args:
            tool_call: The tool call to execute

        Returns:
            ToolResult: The result of the tool execution
        """
        try:
            tool = TOOLS[tool_call.tool_name]
        except KeyError:
            # Tool not found in registry - this is a critical error
            # that should be handled at a higher level
            raise ValueError(f"Tool '{tool_call.tool_name}' not found in registry")

        result = tool(**tool_call.args)

        return ToolResult(
            tool_name=tool_call.tool_name,
            result=result,
        )

    def apply_tool_result(self, tool_result: ToolResult):
        """
        Apply the result of a tool execution to the agent's state.

        Currently only handles 'list_files' tool results.

        Args:
            tool_result: The result of a tool execution
        """
        if tool_result.tool_name == "list_files":
            self.state.files_seen.update(tool_result.result)
            self.state.observations.append(
                f"Discovered {len(tool_result.result)} files"
            )
        else:
            # No handling for other tool types - this may need to be extended
            # in the future based on the agent's requirements
            pass

    def run_step(self, tool_call: ToolCall) -> ToolResult:
        """
        Execute a single step of the agent's workflow.

        Args:
            tool_call: The tool call to execute

        Returns:
            ToolResult: The result of the tool execution
        """
        tool_result = self.execute_tool(tool_call)
        self.apply_tool_result(tool_result)
        return tool_result