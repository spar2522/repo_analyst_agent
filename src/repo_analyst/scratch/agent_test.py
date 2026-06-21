from repo_analyst.agent.agent import Agent
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.hardcoded_planner import HardcodedPlanner
from repo_analyst.tool_call import ToolCall
import logging

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"

logging.basicConfig(level=logging.INFO, format="%(message)s")


def test_list_files():
    """Test the list_files tool by listing all files in the repository."""
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
    logging.info("List files result: %s", result)


def test_search_text():
    """Test the search_text tool by searching for 'redis' in the repository."""
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
    logging.info("Search text result: %s", result)


def test_run_step():
    """Test the run_step method by executing the list_files tool manually."""
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
    logging.info("Run step result: %s", result)
    logging.info("Agent state after step execution:")
    logging.info(state)


def test_agent_run():
    """Test the full agent run with a hardcoded planner for deterministic execution."""
    state = AgentState(
        question="How does Redis work?",
        repo_path="/Users/arpitratan/ai-lab/ai_autodoc",
    )
    planner = (
        HardcodedPlanner()
    )  # Using hardcoded planner for deterministic test execution
    agent = Agent(
        state=state,
        planner=planner,
    )
    agent.run()


if __name__ == "__main__":
    # Set the test name to run. Options: "list_files", "search_text", "run_step", "test_agent_run"
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
