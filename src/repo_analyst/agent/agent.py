from repo_analyst import tool_call
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.tools.tools_registry import TOOLS
from repo_analyst.tool_result import ToolResult


class Agent:
    """Represents an agent that interacts with tools to analyze a repository."""

    def __init__(
        self,
        state: AgentState,
        planner: Planner,
    ):
        """Initialize the agent with the given state and planner.

        Args:
            state: The agent's current state.
            planner: The planner that determines the next tool to call.
        """
        self.state = state
        self.planner = planner

    def execute_tool(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:
        """Execute the given tool call and return the result.

        Args:
            tool_call: The tool call to execute.

        Returns:
            The result of the tool execution.
        """
        tool = TOOLS[tool_call.tool_name]
        result = tool(**tool_call.args)
        return ToolResult(
            tool_name=tool_call.tool_name,
            result=result,
            tool_call=tool_call,
        )

    def apply_tool_result(
        self,
        tool_result: ToolResult,
    ):
        """Apply the result of a tool execution to the agent's state.

        Args:
            tool_result: The result of the tool execution.
        """
        if tool_result.tool_name == "list_files":
            self._handle_list_files(tool_result)
        elif tool_result.tool_name == "search_text":
            self._handle_search_text(tool_result)
        elif tool_result.tool_name == "read_file":
            self._handle_read_file(tool_result)

    def _handle_list_files(self, tool_result: ToolResult):
        """Handle the result of a list_files tool execution."""
        self.state.files_seen.update(tool_result.result)
        self.state.observations.append(f"Discovered {len(tool_result.result)} files")

    def _handle_search_text(self, tool_result: ToolResult):
        """Handle the result of a search_text tool execution."""
        self.state.search_results.update(tool_result.result)
        self.state.observations.append(f"Found {len(tool_result.result)} matching files")

    def _handle_read_file(self, tool_result: ToolResult):
        """Handle the result of a read_file tool execution."""
        file_path = tool_result.tool_call.args["file_path"]
        self.state.files_read.add(file_path)
        self.state.observations.append(f"Read {file_path}")

    def run_step(self, tool_call: ToolCall) -> ToolResult:
        """Run a single step of the agent's execution.

        Args:
            tool_call: The tool call to execute.

        Returns:
            The result of the tool execution.
        """
        tool_result = self.execute_tool(tool_call)
        self.apply_tool_result(tool_result)
        return tool_result

    def run(self):
        """Run the agent until the planner has no more tool calls to make."""
        while True:
            tool_call = self.planner.next_tool_call(self.state)
            if tool_call is None:
                break
            self.run_step(tool_call)