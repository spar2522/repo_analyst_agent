import logging

from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.planner.query_extractor import extract_search_term
from repo_analyst.database.file_summary_repository import (
    FileSummaryRepository,
)
from repo_analyst.search.summary_search import SummarySearch

MAX_FILES_TO_READ = 5


class HardcodedPlanner(Planner):
    """A planner that uses hardcoded logic to determine the next tool call based on the agent's state."""

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.file_summary_repository = FileSummaryRepository()
        self.summary_search = SummarySearch()

    async def next_tool_call(
        self,
        state: AgentState,
    ) -> ToolCall | None:
        """Determine the next tool call based on the agent's state.

        The planner follows a sequence of steps:
        1. If no files have been seen, list all files in the repository.
        2. If the search hasn't been completed, perform a search based on the question.
        3. If search results are not available, return None.
        4. If the maximum number of files to read has been reached, return None.
        5. If there are unread files, read the first one.
        6. If no further actions are needed, return None.

        Args:
            state: The current state of the agent.

        Returns:
            The next ToolCall to execute, or None if no further action is needed.
        """

        if not state.summary_search_completed:

            self.logger.info("Planner: Searching indexed summaries")

            summaries = await self.file_summary_repository.get_all_summaries(
                state.repo_path
            )

            state.relevant_summaries = await self.summary_search.search(
                question=state.question,
                summaries=summaries,
            )

            state.summary_search_completed = True

            self.logger.info(
                f"Planner: Found "
                f"{len(state.relevant_summaries)} "
                f"candidate summaries"
            )

            if state.relevant_summaries:
                top_score = state.relevant_summaries[0][0]
                if top_score >= 3:
                    self.logger.info("Planner: Summary search " "looks good.")
                    state.findings = state.findings_from_summaries()
                    return None

        # First, if no files have been seen, list the files in the repository
        if not state.files_seen:
            self.logger.info("Planner: Looking for all the files in repository")
            return ToolCall(
                tool_name="list_files",
                args={
                    "repo_path": state.repo_path,
                },
            )

        # If the search hasn't been completed yet, perform a search based on the question
        if not state.search_completed:
            search_term = extract_search_term(state.question)
            self.logger.info(
                f"Planner:  Searching repository for files matching {search_term}."
            )
            return ToolCall(
                tool_name="search_text",
                args={
                    "repo_path": state.repo_path,
                    "search_term": search_term,
                },
            )

        # Ensure that search results are available
        if not state.search_results:
            return None

        # If the maximum number of files to read has been reached, return None
        if len(state.files_read) >= MAX_FILES_TO_READ:
            return None

        # Find files that have been searched but not yet read
        unread_files = [
            file for file in state.search_results if file not in state.files_read
        ]

        # If there are unread files, read the first one
        if unread_files:
            self.logger.info(
                f"Planner:  Reading file : {unread_files[0]} out of {len(unread_files)} unread files."
            )
            return ToolCall(
                tool_name="read_file",
                args={
                    "repo_path": state.repo_path,
                    "file_path": unread_files[0],
                },
            )

        # No more actions needed
        return None
