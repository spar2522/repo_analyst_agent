from repo_analyst.agent.agent import Agent
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.tool_call import ToolCall

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"


def test_list_files():

    state = AgentState(question="What files exist?")

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

    state = AgentState(question="How does Redis work?")

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

    state = AgentState(question="What files exist?")

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


if __name__ == "__main__":

    TEST_TO_RUN = "run_step"

    if TEST_TO_RUN == "list_files":
        test_list_files()

    elif TEST_TO_RUN == "search_text":
        test_search_text()

    elif TEST_TO_RUN == "run_step":
        test_run_step()

    else:
        raise ValueError(f"Unknown test: {TEST_TO_RUN}")
