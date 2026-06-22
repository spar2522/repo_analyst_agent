import asyncio

from repo_analyst.agent.agent import Agent
from repo_analyst.agent.agent_state import AgentState
from repo_analyst.planner.hardcoded_planner import HardcodedPlanner
from repo_analyst.tool_call import ToolCall
import logging

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"

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


async def test_search_text():
    """Test the search_text tool by searching for 'redis' in the repository."""
    state = AgentState(question="How does Redis work?")
    agent = Agent(state)
    result = await agent.execute_tool(
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
    """Test the full agent workflow with a hardcoded planner."""
    state = AgentState(question="What is the project structure?")
    agent = Agent(state)
    planner = HardcodedPlanner()
    result = await agent.run(planner)
    logging.info("Test Agent Run - Result: %s", result)


if __name__ == "__main__":
    TEST_SUITE = {
        "list_files": test_list_files,
        "search_text": test_search_text,
        "run_step": test_run_step,
        "agent_run": test_agent_run,
    }

    TEST_NAME = "agent_run"
    test_function = TEST_SUITE[TEST_NAME]
    asyncio.run(test_function())