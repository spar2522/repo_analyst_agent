import asyncio

from repo_analyst.agent.agent import Agent
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.hardcoded_planner import HardcodedPlanner
from repo_analyst.tool_call import ToolCall
import logging

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"
QUESTIONS = {
    "webhook": "Why are webhooks used?",
    "redis": "How is Redis used in this repository?",
    "worker": "How are background workers implemented?",
    "github": "How does GitHub integration work?",
    "review": "How does AutoDoc review code?",
    "pr": "How are pull requests created?",
    "queue": "How are tasks queued and processed?",
    "api": "How is FastAPI used in this project?",
    "architecture": "Explain the architecture of this repository.",
    "flow": "What happens when code is pushed to GitHub?",
    "entrypoint": "What are the main entry points of this application?",
    "storage": "How is data persisted in the system?",
}

logging.basicConfig(level=logging.INFO, format="%(message)s")


async def test_list_files():
    """Test the list_files tool by listing all files in the repository."""
    state = AgentState(question="What files exist?")
    agent = Agent(state)
    result = await agent.execute_tool(
        ToolCall(
            tool_name="list_files",
            args={
                "repo_path": REPO_PATH,
            },
        )
    )
    logging.info("Test List Files - Result: %s", result)


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
    logging.info("Test Search Text - Result: %s", result)


async def test_run_step():
    """Test the run_step method by executing the list_files tool manually."""
    state = AgentState(question="What files exist?")
    agent = Agent(state)
    result = await agent.run_step(
        ToolCall(
            tool_name="list_files",
            args={
                "repo_path": REPO_PATH,
            },
        )
    )
    logging.info("Test Run Step - Result: %s", result)
    logging.info("Agent state after step execution:")
    logging.info(state)


async def test_agent_run():
    """Test the full agent run with a hardcoded planner for deterministic execution."""

    q = QUESTIONS["worker"]

    logging.info("=" * 60)
    logging.info(f"Question : {q}")
    logging.info("=" * 60)

    state = AgentState(
        question=q,
        repo_path=REPO_PATH,
    )

    planner = (
        HardcodedPlanner()
    )  # Using hardcoded planner for deterministic test execution
    agent = Agent(
        state=state,
        planner=planner,
    )
    await agent.run()


if __name__ == "__main__":
    # Set the test name to run. Options: "list_files", "search_text", "run_step", "test_agent_run"
    # Modify TEST_NAME below to select which test to execute
    TEST_NAME = "test_agent_run"
    test_functions = {
        "list_files": test_list_files,
        "search_text": test_search_text,
        "run_step": test_run_step,
        "test_agent_run": test_agent_run,
    }

    if TEST_NAME in test_functions:
        asyncio.run(test_functions[TEST_NAME]())
    else:
        raise ValueError(f"Unknown test: {TEST_NAME}")
