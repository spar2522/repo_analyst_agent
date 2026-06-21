from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.tools.tools_registry import TOOLS
from repo_analyst.tool_result import ToolResult
import logging


class Agent:
    def __init__(
        self,
        state: AgentState,
        planner: Planner,
    ):
        """Initialize the Agent with the given state and planner."""
        self.state = state
        self.planner = planner
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Map tool names to their corresponding result handlers
        self.handlers = {
            "list_files": self._handle_list_files,
            "search_text": self._handle_search_text,
            "read_file": self._handle_read_file,
        }

    def execute_tool(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:
        """Execute the specified tool and return the result."""
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
        """Apply the result of a tool execution to the agent state."""
        handler = self.handlers.get(tool_result.tool_name)
        if handler:
            handler(tool_result)
        else:
            self.logger.warning(f"No handler found for tool: {tool_result.tool_name}")

    def _handle_list_files(self, tool_result: ToolResult):
        """Handle the result of a list_files tool execution."""
        self.state.files_seen.update(tool_result.result)
        self.state.observations.append(f"Discovered {len(tool_result.result)} files")

    def _handle_search_text(self, tool_result: ToolResult):
        """Handle the result of a search_text tool execution."""
        self.state.search_results.update(tool_result.result)
        self.state.search_completed = True  # Signal that search phase is complete

        self.state.observations.append(
            f"Found {len(tool_result.result)} matching files"
        )

    def _handle_read_file(self, tool_result: ToolResult):
        """Handle the result of a read_file tool execution."""
        file_path = tool_result.tool_call.args["file_path"]
        self.state.files_read.add(file_path)
        self.state.observations.append(f"Read {file_path}")

    def run_step(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:
        """Execute a single step of the agent's workflow."""
        self.logger.info("")
        self.logger.info("=" * 60)
        self.logger.info(f"Executing Tool: {tool_call.tool_name}")
        self.logger.info("=" * 60)
        self.logger.info(f"Arguments: {tool_call.args}")
        tool_result = self.execute_tool(tool_call)
        self.logger.info("Tool execution completed")

        self.apply_tool_result(tool_result)
        self.log_state()

        return tool_result

    def run(self):
        """Run the agent until the planner indicates completion."""
        self.logger.info("Agent started")
        while True:
            tool_call = self.planner.next_tool_call(self.state)
            if tool_call is None:
                self.logger.info("Agent workflow completed.")
                break
            self.run_step(tool_call)

    def log_state(self):
        """Log the current state of the agent."""
        summary = self.state.summary()

        self.logger.info("")
        self.logger.info("STATE")
        self.logger.info("-" * 40)

        for key, value in summary.items():
            self.logger.info(f"{key}: {value}")

        self.logger.info("")

        self.logger.info("Recent Observations:")

        for observation in self.state.observations[-5:]:
            self.logger.info(f"  - {observation}")