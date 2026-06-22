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
        self.llm_client = LLMClient()
        self.file_summarizer = FileSummarizer(self.llm_client)
        self.file_summary_repo = FileSummaryRepository()
        self.agent_run_repo = AgentRunRepository()
        self.agent_finding_repo = AgentFindingRepository()

        self.handlers = {
            "read_file": self._handle_read_file,
        }

    async def execute_tool(self, tool_call: ToolCall) -> dict:
        """Execute the specified tool with the given parameters."""
        try:
            tool = TOOLS[tool_call.tool_name]
            result = await tool(**tool_call.parameters)
            return {"status": "success", "result": result}
        except Exception as e:
            logging.error(f"Error executing tool {tool_call.tool_name}: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def apply_tool_result(self, tool_call: ToolCall, result: dict):
        """Apply the result of a tool execution."""
        try:
            handler = self.handlers.get(tool_call.tool_name)
            if handler:
                await handler(tool_call, result)
            else:
                logging.warning(f"No handler found for tool {tool_call.tool_name}")
        except Exception as e:
            logging.error(f"Error applying tool result for {tool_call.tool_name}: {str(e)}")

    async def _handle_read_file(self, tool_call: ToolCall, result: dict):
        """Handle the result of a file read operation."""
        try:
            file_content = result.get("result")
            if not file_content:
                logging.warning("No content received from file read operation")
                return

            file_path = tool_call.parameters.get("file_path")
            if not file_path:
                logging.warning("File path missing in tool call parameters")
                return

            # Check for existing summary
            existing_summary = await self.file_summary_repo.get_summary(file_path)
            if existing_summary:
                logging.info(f"Using cached summary for {file_path}")
                self.state.add_result("summary", existing_summary)
                return

            # Generate new summary
            summary = await self.file_summarizer.summarize(
                file_path=file_path,
                content=file_content,
            )
            await self.file_summary_repo.save_summary(file_path, summary)
            logging.info(f"Saved new summary for {file_path}")
            self.state.add_result("summary", summary)

        except Exception as e:
            logging.error(f"Error handling file read for {file_path}: {str(e)}")

    async def run_step(self, tool_call: ToolCall):
        """Execute a single step in the agent workflow."""
        try:
            logging.info(f"Executing tool {tool_call.tool_name}")
            result = await self.execute_tool(tool_call)
            await self.apply_tool_result(tool_call, result)
            return result
        except Exception as e:
            logging.error(f"Error in run step for {tool_call.tool_name}: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def run(self):
        """Run the agent workflow."""
        try:
            logging.info("Starting agent workflow")
            self.state.start_timer()

            # Create agent run record
            run_id = await self.agent_run_repo.create_run(self.state)
            self.state.run_id = run_id

            # Execute all steps
            for step in self.planner.get_steps():
                result = await self.run_step(step)
                if result["status"] != "success":
                    logging.error(f"Step {step.tool_name} failed: {result['message']}")
                    break

            # Generate final answer
            answer = await self.answer_generator.generate(self.state)
            await self.agent_finding_repo.save_finding(run_id, answer)
            logging.info("Agent workflow completed successfully")

        except Exception as e:
            logging.error(f"Critical error in agent workflow: {str(e)}")
            return {"status": "error", "message": str(e)}

        finally:
            self.state.stop_timer()
            logging.info(f"Agent workflow completed in {self.state.duration:.2f} seconds")