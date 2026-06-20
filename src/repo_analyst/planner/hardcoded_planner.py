from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall


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

        if not state.search_results:
            return ToolCall(
                tool_name="search_text",
                args={
                    "repo_path": state.repo_path,
                    "search_term": "redis",
                },
            )

        for file in state.search_results:
            if file not in state.files_read:

                return ToolCall(
                    tool_name="read_file",
                    args={
                        "repo_path": state.repo_path,
                        "file_path": file,
                    },
                )

        return None
