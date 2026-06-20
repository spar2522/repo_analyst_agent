from repo_analyst import tool_call
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.planner import Planner
from repo_analyst.tool_call import ToolCall
from repo_analyst.tools.tools_registry import TOOLS
from repo_analyst.tool_result import ToolResult


class Agent:

    def __init__(
        self,
        state: AgentState,
        planner: Planner,
    ):
        self.state = state
        self.planner = planner

    def execute_tool(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:

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

        if tool_result.tool_name == "list_files":

            self.state.files_seen.update(tool_result.result)

            self.state.observations.append(
                f"Discovered {len(tool_result.result)} files"
            )
        elif tool_result.tool_name == "search_text":
            self.state.search_results.update(tool_result.result)

            self.state.observations.append(
                f"Found {len(tool_result.result)} matching files"
            )

        elif tool_result.tool_name == "read_file":

            file_path = tool_result.tool_call.args["file_path"]

            self.state.files_read.add(file_path)

            self.state.observations.append(f"Read {file_path}")

    def run_step(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:

        tool_result = self.execute_tool(tool_call)

        self.apply_tool_result(tool_result)

        return tool_result

    def run(self):

        while True:

            tool_call = self.planner.next_tool_call(self.state)

            if tool_call is None:
                break

            self.run_step(tool_call)
