import logging
import time

from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.planner.query_extractor import extract_search_term
from repo_analyst.retrieval.repository_retriever import (
    RepositoryRetriever,
)

MAX_FILES_TO_READ = 5
HYBRID_CONFIDENCE_THRESHOLD = 0.75


class HardcodedPlanner(Planner):
    """A planner that uses hardcoded logic to determine the next tool call based on the agent's state."""

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.repository_retriever = RepositoryRetriever()

    async def next_tool_call(
        self,
        state: AgentState,
    ) -> ToolCall | None:
        """Determine the next tool call based on the agent's state.

        The planner follows these steps in order:
        1. If the summary search hasn't been completed, perform it.
        2. If no files have been seen, list all files in the repository.
        3. If the text search hasn't been completed, perform it.
        4. If the maximum number of files to read has been reached, return None.
        5. If there are unread files, read the first one.
        6. If no further actions are needed, return None.

        Args:
            state: The current state of the agent.

        Returns:
            The next ToolCall to execute, or None if no further action is needed.
        """

        await self._handle_retrieval(state)
        if self._is_retrieval_sufficient(state):
            self.logger.info("*" * 60)
            self.logger.info("*" * 60)
            self.logger.info(f"Retrieval data enough, proceeding to answer")
            self.logger.info("*" * 60)
            self.logger.info("*" * 60)
            time.sleep(3)

            state.findings = state.findings_from_summaries()
            return None

        if not state.files_seen:
            self.logger.info("*" * 60)
            self.logger.info("*" * 60)
            self.logger.info(f"RETRIEVAL DATA INSUFFICIENT")
            self.logger.info("*" * 60)
            self.logger.info("*" * 60)
            time.sleep(3)
            return self._handle_file_listing(state)

        if not state.search_completed:
            return self._handle_text_search(state)

        if not state.search_results:
            return None

        if len(state.files_read) >= MAX_FILES_TO_READ:
            return None

        return self._handle_file_reading(state)

    async def _handle_retrieval(self, state: AgentState) -> None:
        """Handle the summary search step if it hasn't been completed."""
        if not state.summary_search_completed:
            self.logger.info("Planner: Searching indexed summaries")

            try:
                state.summary_search_completed = True
                state.relevant_summaries = await self.repository_retriever.retrieve(
                    repo_path=state.repo_path,
                    question=state.question,
                )
            except Exception as e:
                self.logger.error(f"Error during summary search: {e}")
                raise

    def _is_retrieval_sufficient(self, state):
        if not state.relevant_summaries:
            return False
        top_score = state.relevant_summaries[0][0]
        return top_score >= HYBRID_CONFIDENCE_THRESHOLD

    def _handle_file_listing(self, state: AgentState) -> ToolCall:
        """Handle the file listing step if no files have been seen."""
        self.logger.info("Planner: Looking for all the files in repository")
        return ToolCall(
            tool_name="list_files",
            args={
                "repo_path": state.repo_path,
            },
        )

    def _handle_text_search(self, state: AgentState) -> ToolCall:
        """Handle the text search step if it hasn't been completed."""
        search_term = extract_search_term(state.question)
        self.logger.info(
            f"Planner: Searching repository for files matching {search_term}."
        )
        return ToolCall(
            tool_name="search_text",
            args={
                "repo_path": state.repo_path,
                "search_term": search_term,
            },
        )

    def _handle_file_reading(self, state: AgentState) -> ToolCall | None:
        """Handle the file reading step if there are unread files."""
        unread_files = [
            file for file in state.search_results if file not in state.files_read
        ]

        if not unread_files:
            return None

        self.logger.info(
            f"Planner: Reading file : {unread_files[0]} out of {len(unread_files)} unread files."
        )
        return ToolCall(
            tool_name="read_file",
            args={
                "repo_path": state.repo_path,
                "file_path": unread_files[0],
            },
        )
