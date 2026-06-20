from abc import ABC
from abc import abstractmethod

from repo_analyst.agent.agent_state import AgentState
from repo_analyst.tool_call import ToolCall


class Planner(ABC):

    @abstractmethod
    def next_tool_call(
        self,
        state: AgentState,
    ) -> ToolCall | None:
        pass
