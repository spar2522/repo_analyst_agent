from repo_analyst.agent.agent_state import AgentState
from repo_analyst.agent.summarizers.file_summarizer import summarize_file
from repo_analyst.llm.answer_generator import AnswerGenerator
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.tools.tools_registry import TOOLS
from repo_analyst.tool_result import ToolResult
from repo_analyst.llm.file_summariser import FileSummarizer
from repo_analyst.llm.llm_client import LLMClient
from repo_analyst.database.file_summary_repository import (
    FileSummaryRepository,
)

from repo_analyst.database.agent_run_repository import (
    AgentRunRepository,
)

from repo_analyst.database.agent_finding_repository import (
    AgentFindingRepository,
)
import logging


class Agent:
    def __init__(
        self,
        state: AgentState,
        planner: Planner,
    ):
        self.state = state
        self.planner = planner
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        llm_client = LLMClient()
        self.file_summarizer = FileSummarizer(llm_client)
        self.answer_generator = AnswerGenerator(llm_client)

        self.handlers = {
            "list_files": self._handle_list_files,
            "search_text": self._handle_search_text,
            "read_file": self._handle_read_file,
        }

        self.agent_run_repository = AgentRunRepository()

        self.agent_finding_repository = AgentFindingRepository()

        self.file_summary_repository = FileSummaryRepository()

    async def execute_tool(
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

    async def apply_tool_result(
        self,
        tool_result: ToolResult,
    ):
        """Apply the result of a tool execution to the agent state."""
        handler = self.handlers.get(tool_result.tool_name)
        if handler:
            await handler(tool_result)
        else:
            self.logger.warning(f"No handler found for tool: {tool_result.tool_name}")

    async def _handle_list_files(self, tool_result: ToolResult):
        """Handle the result of a list_files tool execution."""
        self.state.files_seen.update(tool_result.result)
        self.state.observations.append(f"Discovered {len(tool_result.result)} files")

    async def _handle_search_text(self, tool_result: ToolResult):
        """Handle the result of a search_text tool execution."""
        self.state.search_results.update(tool_result.result)
        self.state.search_completed = True

        self.state.observations.append(
            f"Found {len(tool_result.result)} matching files"
        )

    async def _handle_read_file(self, tool_result: ToolResult):
        """Handle the result of a read_file tool execution."""
        file_path = tool_result.tool_call.args["file_path"]
        self.state.files_read.add(file_path)
        self.logger.info(f"File Size: {len(tool_result.result)} chars")

        existing_summary = await self.file_summary_repository.get_summary(
            self.state.repo_path,
            file_path,
        )

        if existing_summary:
            self.logger.info(f"⚡ Loaded cached summary: {file_path}")
            summary = existing_summary.summary

        else:
            summary = await self.file_summarizer.summarize(
                file_path=file_path,
                content=tool_result.result,
            )
            await self.file_summary_repository.save_summary(
                repo_path=self.state.repo_path,
                file_path=file_path,
                summary=summary,
            )

        self.state.findings.append(summary)

        await self.agent_finding_repository.save_finding(
            run_id=self.state.run_id,
            file_path=file_path,
            finding=summary,
        )

        self.logger.info("Finding persisted")
        self.state.observations.append(f"Read {file_path}")

    async def run_step(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:
        """Execute a single step of the agent's workflow."""
        self.logger.info("")
        self.logger.info("=" * 60)
        self.logger.info(f"Executing Tool: {tool_call.tool_name}")
        self.logger.info("=" * 60)
        self.logger.info(f"Arguments: {tool_call.args}")
        tool_result = await self.execute_tool(tool_call)
        self.logger.info("Tool execution completed")

        await self.apply_tool_result(tool_result)
        await self.log_state()

        return tool_result

    async def run(self):
        """Run the agent until the planner indicates completion."""
        run = await self.agent_run_repository.create_run(
            question=self.state.question,
            repo_path=self.state.repo_path,
        )
        self.state.run_id = run.id
        self.logger.info(f"Created Agent Run: {run.id}")

        self.logger.info("Agent started")
        while True:
            tool_call = self.planner.next_tool_call(self.state)
            if tool_call is None:
                self.logger.info("Agent workflow completed.")
                break
            await self.run_step(tool_call)

        answer = self.answer_generator.generate(
            question=self.state.question,
            findings=self.state.findings,
        )

        self.state.final_answer = answer

        self.logger.info("")
        self.logger.info("FINAL ANSWER")
        self.logger.info("=" * 60)
        self.logger.info(answer)

    async def log_state(self):

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

        self.logger.info("")

        self.logger.info("Recent Findings:")

        for observation in self.state.findings:

            self.logger.info(f"  - {observation}")
