from repo_analyst.agent.agent_state import AgentState
from repo_analyst.agent.summarizers.file_summarizer import summarize_file
from repo_analyst.llm.answer_generator import AnswerGenerator
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.tools.tools_registry import TOOLS
from repo_analyst.tool_result import ToolResult
from repo_analyst.llm.file_summarizer import FileSummarizer
from repo_analyst.llm.llm_client import LLMClient
import asyncio

from repo_analyst.database.agent_run_repository import (
    AgentRunRepository,
)
from repo_analyst.database.agent_finding_repository import (
    AgentFindingRepository,
)

class Agent:
    def __init__(self, planner: Planner, state: AgentState):
        self.planner = planner
        self.state = state
        self.llm_client = LLMClient()
        self.file_summarizer = FileSummarizer(self.llm_client)
        self.answer_generator = AnswerGenerator(self.llm_client)
        self.agent_run_repository = AgentRunRepository()
        self.agent_finding_repository = AgentFindingRepository()

    def execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call and return the result."""
        return tool_call.execute()

    def apply_tool_result(self, tool_result: ToolResult):
        """Apply the result of a tool call to the agent's state."""
        if tool_result.handler in self.state.handlers:
            self.state.handlers[tool_result.handler](tool_result)
        else:
            self.logger.warning(f"No handler found for tool result: {tool_result}")

    def _handle_read_file(self, tool_result: ToolResult):
        """Handle the result of a file read operation."""
        file_content = tool_result.data
        summary = self.file_summarizer.summarize(file_content)
        self.state.findings.append(summary)
        self.agent_finding_repository.save_finding(summary)

    def run(self):
        """Run the agent's main loop."""
        self.agent_run_repository.create_run(self.state)
        while True:
            tool_call = self.planner.get_next_tool_call()
            if tool_call is None:
                break
            tool_result = self.execute_tool(tool_call)
            self.apply_tool_result(tool_result)

        answer = self.answer_generator.generate(self.state.findings)
        self.state.final_answer = answer
        self.agent_run_repository.update_run(self.state, answer)

    def log_state(self):
        """Log the current state of the agent."""
        self.logger.info("Agent State:")
        self.logger.info(f"Current State: {self.state}")
        self.logger.info("Recent Observations:")
        for observation in self.state.observations[-5:]:
            self.logger.info(f"- {observation}")
        self.logger.info("Recent Findings:")
        for finding in self.state.findings[-5:]:
            self.logger.info(f"- {finding}")