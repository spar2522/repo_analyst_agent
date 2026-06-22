import logging

from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.planner.query_extractor import (
    extract_search_term,
)

MAX_FILES_TO_READ = 5


class HardcodedPlanner(Planner):
    """A planner that uses hardcoded logic to determine the next tool call based on the agent's state."""

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def next_tool_call(
        self,
        state: AgentState,
    ) -> ToolCall | None:
        """Determine the next tool call based on the agent's state.

        Args:
            state: The current state of the agent.

        Returns:
            The next ToolCall to execute, or None if no further action is needed.
        """

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
