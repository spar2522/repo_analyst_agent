from repo_analyst.agent.agent import Agent
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.hardcoded_planner import HardcodedPlanner
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


def test_agent_run():
    state = AgentState(
        question="What files exist?",
        repo_path="/Users/arpitratan/ai-lab/ai_autodoc",
    )
    planner = HardcodedPlanner()  # Using hardcoded planner for deterministic test execution
    agent = Agent(
        state=state,
        planner=planner,
    )
    agent.run()


if __name__ == "__main__":
    TEST_NAME = "test_agent_run"
    test_functions = {
        "list_files": test_list_files,
        "search_text": test_search_text,
        "run_step": test_run_step,
        "test_agent_run": test_agent_run,
    }

    if TEST_NAME in test_functions:
        test_functions[TEST_NAME]()
    else:
        raise ValueError(f"Unknown test: {TEST_NAME}")