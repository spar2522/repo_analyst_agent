from repo_analyst.agent.agent import Agent
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.hardcoded_planner import HardcodedPlanner
from repo_analyst.tool_call import ToolCall

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"


def test_list_files():
    """Test the Agent's ability to list files in the repository."""
    state = AgentState(
        question="What files exist?",
        repo_path=REPO_PATH,
    )

    agent = Agent(state)

    result = agent.execute_tool(
        ToolCall(
            tool_name="list_files",
            args={
                "repo_path": REPO_PATH,
            },
        )
    )

    print(result)


def test_search_text():
    """Test the Agent's ability to search for text in the repository."""
    state = AgentState(
        question="How does Redis work?",
        repo_path=REPO_PATH,
    )

    agent = Agent(state)

    result = agent.execute_tool(
        ToolCall(
            tool_name="search_text",
            args={
                "repo_path": REPO_PATH,
                "search_term": "redis",
            },
        )
    )

    print(result)


def test_run_step():
    """Test the Agent's ability to run a single step with a specific tool call."""
    state = AgentState(
        question="What files exist?",
        repo_path=REPO_PATH,
    )

    agent = Agent(state)

    result = agent.run_step(
        ToolCall(
            tool_name="list_files",
            args={
                "repo_path": REPO_PATH,
            },
        )
    )

    print(result)
    print()
    print("STATE")
    print(state)


def test_agent_run():
    """Test the Agent's full execution flow with a hardcoded planner."""
    state = AgentState(
        question="What files exist?",
        repo_path=REPO_PATH,
    )

    planner = HardcodedPlanner()

    agent = Agent(
        state=state,
        planner=planner,
    )

    agent.run()

    print(state)


if __name__ == "__main__":

    TEST_TO_RUN = "test_agent_run"

    if TEST_TO_RUN == "list_files":
        test_list_files()

    elif TEST_TO_RUN == "search_text":
        test_search_text()

    elif TEST_TO_RUN == "run_step":
        test_run_step()

    elif TEST_TO_RUN == "test_agent_run":
        test_agent_run()

    else:
        raise ValueError(f"Unknown test: {TEST_TO_RUN}")