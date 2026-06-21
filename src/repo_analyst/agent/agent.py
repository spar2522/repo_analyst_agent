from repo_analyst.agent.agent_state import AgentState
from repo_analyst.agent.summarizers.file_summarizer import summarize_file
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
        """Initialize the Agent with its state and planner.

        Args:
            state: The AgentState object that tracks the agent's progress.
            planner: The Planner object that determines the next tool to execute.
        """
        self.state = state
        self.planner = planner
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.handlers = {
            "list_files": self._handle_list_files,
            "search_text": self._handle_search_text,
            "read_file": self._handle_read_file,
        }

    def execute_tool(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:
        """Execute the specified tool and return the result.

        Args:
            tool_call: The ToolCall object specifying which tool to execute and with what arguments.

        Returns:
            The ToolResult object containing the result of the tool execution.
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
        """Apply the result of a tool execution to the agent state.

        Args:
            tool_result: The ToolResult object containing the result of the tool execution.
        """
        handler = self.handlers.get(tool_result.tool_name)
        if handler:
            handler(tool_result)
        else:
            self.logger.warning(f"No handler found for tool: {tool_result.tool_name}")

    def _handle_list_files(self, tool_result: ToolResult):
        """Handle the result of a list_files tool execution.

        Adds discovered files to the state and logs the number of files discovered.
        """
        self.state.files_seen.update(tool_result.result)
        self.state.observations.append(f"Discovered {len(tool_result.result)} files")

    def _handle_search_text(self, tool_result: ToolResult):
        """Handle the result of a search_text tool execution.

        Updates the state with search results and logs the number of matches found.
        """
        self.state.search_results.update(tool_result.result)
        self.state.observations.append(f"Found {len(tool_result.result)} matches")

    def _handle_read_file(self, tool_result: ToolResult):
        """Handle the result of a read_file tool execution.

        Summarizes the file content and adds the summary to the state's findings.
        """
        file_path = tool_result.tool_call.args.get("file_path")
        content = tool_result.result

        try:
            summary = summarize_file(file_path=file_path, content=content)
        except Exception as e:
            self.logger.error(f"Error summarizing file {file_path}: {e}")
            summary = "Summary unavailable due to an error"

        self.state.findings.append(summary)
        self.state.observations.append(f"Read and summarized file: {file_path}")

    def run(self):
        """Run the agent until no further tools are needed."""
        while self.planner.has_next_tool():
            tool_call = self.planner.next_tool()
            self.logger.info(f"Executing tool: {tool_call.tool_name}")
            tool_result = self.execute_tool(tool_call)
            self.apply_tool_result(tool_result)
            self.logger.info("Tool execution completed.")

    def log_state(self):
        """Log the current state of the agent, including observations and findings."""
        summary = self.state.summary()
        self.logger.info("Current Agent State:")
        for key, value in summary.items():
            self.logger.info(f"{key}: {value}")

        self.logger.info("\nRecent Observations:")
        for observation in self.state.observations[-5:]:
            self.logger.info(f"- {observation}")

        self.logger.info("\nRecent Findings:")
        for finding in self.state.findings[-5:]:
            self.logger.info(f"- {finding}")