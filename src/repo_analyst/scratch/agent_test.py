from repo_analyst.agent.agent import Agent
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.tool_call import ToolCall

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"


def _execute_tool_test(question, tool_name, args):
    """Execute a tool test with the given parameters.

    Args:
        question: The question to be processed by the agent.
        tool_name: Name of the tool to execute.
        args: Arguments for the tool call.

    Returns:
        Result of the tool execution.
    """
    state = AgentState(question=question)
    agent = Agent(state)
    result = agent.execute_tool(
        ToolCall(tool_name=tool_name, args=args)
    )
    return result


def test_list_files():
    """Test listing files in the repository."""
    result = _execute_tool_test(
        question="What files exist?",
        tool_name="list_files",
        args={"repo_path": REPO_PATH},
    )
    print("Test List Files Result:")
    print(result)


def test_search_text():
    """Test searching text in the repository."""
    result = _execute_tool_test(
        question="How does Redis work?",
        tool_name="search_text",
        args={"repo_path": REPO_PATH, "search_term": "redis"},
    )
    print("Test Search Text Result:")
    print(result)


def test_run_step():
    """Test running a single step with state tracking."""
    state = AgentState(question="What files exist?")
    agent = Agent(state)
    result = agent.run_step(
        ToolCall(
            tool_name="list_files",
            args={"repo_path": REPO_PATH},
        )
    )
    print("Test Run Step Result:")
    print(result)
    print()
    print("Agent State After Step:")
    print(state)


if __name__ == "__main__":
    # Select which test to run
    TEST_TO_RUN = "run_step"

    if TEST_TO_RUN == "list_files":
        test_list_files()

    elif TEST_TO_RUN == "search_text":
        test_search_text()

    elif TEST_TO_RUN == "run_step":
        test_run_step()

    else:
        raise ValueError(f"Unknown test: {TEST_TO_RUN}")