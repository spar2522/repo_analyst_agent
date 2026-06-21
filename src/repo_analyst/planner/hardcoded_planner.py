from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.planner.query_extractor import (
    extract_search_term,
)

MAX_FILES_TO_READ = 5


class HardcodedPlanner(Planner):

    def next_tool_call(
        self,
        state: AgentState,
    ) -> ToolCall | None:

        if not state.files_seen:

            return ToolCall(
                tool_name="list_files",
                args={
                    "repo_path": state.repo_path,
                },
            )

        if not state.search_completed:
            return ToolCall(
                tool_name="search_text",
                args={
                    "repo_path": state.repo_path,
                    "search_term": extract_search_term(state.question),
                },
            )

        if len(state.files_read) >= MAX_FILES_TO_READ:
            return None

        unread_files = [
            file for file in state.search_results if file not in state.files_read
        ]

        if unread_files:
            return ToolCall(
                tool_name="read_file",
                args={
                    "repo_path": state.repo_path,
                    "file_path": unread_files[0],
                },
            )

        return None
