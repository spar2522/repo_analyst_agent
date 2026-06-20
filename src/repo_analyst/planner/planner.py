from abc import ABC
from abc import abstractmethod

from repo_analyst.agent.agent_state import AgentState
from repo_analyst.tool_call import ToolCall


class Planner(ABC):
    """Abstract base class for planning tool calls in an agent's workflow.

    Subclasses must implement the next_tool_call method to determine
    which tool should be called next based on the agent's current state.
    """

    @abstractmethod
    def next_tool_call(
        self,
        state: AgentState,
    ) -> ToolCall | None:
        """Determine the next tool call based on the agent's current state.

        Args:
            state: The current state of the agent, containing all relevant
                information needed to make a planning decision.

        Returns:
            A ToolCall object representing the next tool to execute, or
            None if no tool should be called at this time.
        """
        pass