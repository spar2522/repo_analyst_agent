from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.tools.tools_registry import TOOLS
from repo_analyst.tool_result import ToolResult
from repo_analyst.llm.file_summariser import FileSummarizer
from repo_analyst.llm.llm_client import LLMClient
import logging


class Agent:
    """Agent class that coordinates tool execution and state management for repository analysis."""

    def __init__(
        self,
        state: AgentState,
        planner: Planner,
    ):
        self.state = state
        self.planner = planner
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.file_summarizer = FileSummarizer(LLMClient())

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
        self.state.observations.append(f"Found {len(tool_result.result)} matches")

    def _handle_read_file(self, tool_result: ToolResult):
        """Handle the result of a read_file tool execution."""
        file_path = tool_result.tool_call.args.get("file_path")
        if not file_path:
            self.logger.error("Missing 'file_path' in tool_call arguments for read_file")
            return

        try:
            content = tool_result.result
            summary = self.file_summarizer.summarize(content)
            self.state.findings.append(summary)
            self.state.observations.append(f"Read and summarized file: {file_path}")
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")

    def run_step(self):
        """Execute a single step of the agent's workflow."""
        tool_call = self.planner.plan(self.state)
        if not tool_call:
            self.logger.info("No tool call planned. Ending workflow.")
            return False

        tool_result = self.execute_tool(tool_call)
        self.apply_tool_result(tool_result)
        return True

    def run(self):
        """Run the agent until the planner indicates completion."""
        while self.run_step():
            pass

    def log_state(self):
        """Log the current state of the agent for debugging and monitoring."""
        self.logger.info("=== Agent State ===")
        self.logger.info(f"Files seen: {len(self.state.files_seen)}")
        self.logger.info(f"Search results: {len(self.state.search_results)}")
        self.logger.info(f"Findings: {len(self.state.findings)}")
        self.logger.info(f"Observations: {self.state.observations[-5:]}")  # Last 5 observations
        self.logger.info("=== End of State ===")