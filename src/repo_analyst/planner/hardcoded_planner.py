from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall


class HardcodedPlanner(Planner):
    """A hardcoded planner that follows a predefined sequence of steps:
    1. List files in the repository
    2. Search for files containing 'redis'
    3. Read each matching file one by one
    """

    SEARCH_TERM = "redis"

    def next_tool_call(
        self,
        state: AgentState,
    ) -> ToolCall | None:
        """Determine the next tool call based on the current agent state.

        Args:
            state: The current state of the agent, containing repository path,
                files seen, search results, and files read.

        Returns:
            The next ToolCall to execute, or None if no further action is needed.
        """

        # First step: List files in the repository if not already done
        if not state.files_seen:
            return ToolCall(
                tool_name="list_files",
                args={
                    "repo_path": state.repo_path,
                },
            )

        # Second step: Search for files containing 'redis' if search hasn't been done
        if not state.search_results:
            return ToolCall(
                tool_name="search_text",
                args={
                    "repo_path": state.repo_path,
                    "search_term": self.SEARCH_TERM,
                },
            )

        # Third step: Read each file from search results that hasn't been read yet
        for file in state.search_results:
            if file not in state.files_read:
                return ToolCall(
                    tool_name="read_file",
                    args={
                        "repo_path": state.repo_path,
                        "file_path": file,
                    },
                )

        # No further actions needed if all files have been processed
        return None