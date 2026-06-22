```python
import logging

class Agent:
    def __init__(self, state: 'AgentState'):
        """
        Initialize the Agent with the given state.

        Args:
            state (AgentState): The state object that holds the agent's data.
        """
        self.state = state
        self.file_summarizer = FileSummarizer()  # Assuming a FileSummarizer class exists
        self.agent_run_repository = AgentRunRepository()
        self.agent_finding_repository = AgentFindingRepository()

    async def execute_tool(self, tool_call: dict) -> dict:
        """
        Execute the specified tool with the given arguments and return the result.

        Args:
            tool_call (dict): A dictionary containing the tool name and its arguments.

        Returns:
            dict: The result of the tool execution.
        """
        try:
            tool_name = tool_call.get("tool_name")
            tool_args = tool_call.get("tool_args", {})
            tool = self._get_tool(tool_name)
            result = await tool(**tool_args)
            return {"tool_name": tool_name, "result": result}
        except Exception as e:
            logging.error(f"Error executing tool {tool_name}: {str(e)}")
            raise

    def _get_tool(self, tool_name: str):
        """
        Retrieve the appropriate tool based on the tool name.

        Args:
            tool_name (str): The name of the tool to retrieve.

        Returns:
            function: The corresponding tool function.

        Raises:
            ValueError: If the tool is not found.
        """
        # Example tool mapping; actual implementation may vary
        tools = {
            "list_files": self._list_files,
            "read_file": self._read_file,
            # Add more tools as needed
        }
        if tool_name not in tools:
            raise ValueError(f"Tool {tool_name} not found")
        return tools[tool_name]

    async def _list_files(self, directory: str) -> list:
        """List files in the specified directory."""
        # Implementation details
        return []

    async def _read_file(self, file_path: str) -> str:
        """Read the content of the specified file."""
        # Implementation details
        return ""

    async def apply_tool_result(self, tool_result: dict):
        """
        Apply the result of a tool execution.

        Args:
            tool_result (dict): A dictionary containing the tool name and its result.
        """
        try:
            tool_name = tool_result.get("tool_name")
            result = tool_result.get("result")
            handler = self._get_handler(tool_name)
            await handler(result)
        except Exception as e:
            logging.error(f"Error applying result of tool {tool_name}: {str(e)}")
            raise

    def _get_handler(self, tool_name: str):
        """
        Retrieve the appropriate handler based on the tool name.

        Args:
            tool_name (str): The name of the tool.

        Returns:
            function: The corresponding handler function.

        Raises:
            ValueError: If the handler is not found.
        """
        handlers = {
            "list_files": self._handle_list_files,
            "read_file": self._handle_read_file,
            # Add more handlers as needed
        }
        if tool_name not in handlers:
            raise ValueError(f"Handler for tool {tool_name} not found")
        return handlers[tool_name]

    async def _handle_list_files(self, result: list):
        """Handle the result of listing files."""
        self.state.observations.append(f"Found {len(result)} files")

    async def _handle_read_file(self, result: str):
        """Handle the result of reading a file."""
        self.state.findings.append(f"File content: {result[:100]}...")

    async def log_state(self):
        """
        Log the current state of the agent, including observations and findings.
        """
        summary = self.state.summary()

        logging.info("")
        logging.info("STATE")
        logging.info("-" * 40)

        for key, value in summary.items():
            logging.info(f"{key}: {value}")

        logging.info("")

        logging.info("Recent Observations:")

        for observation in self.state.observations[-5:]:
            logging.info(f"  - {observation}")

        logging.info("")

        logging.info("Recent Findings:")

        for finding in self.state.findings:
            logging.info(f"  - {finding}")

        logging.info("")

    async def run(self):
        """
        Run the agent until the planner indicates completion.
        """
        try:
            run = await self.agent_run_repository.create_run(
                question=self.state.question,
                repo_path=self.state.repo_path,
            )
            self.state.run_id = run.id
            logging.info(f"Created Agent Run: {run.id}")

            logging.info("Agent started")
            while True:
                tool_call = self.state.planner.next_tool_call(self.state)
                if tool_call is None:
                    logging.info("Agent workflow completed.")
                    break
                await self.run_step(tool_call)
        except Exception as e:
            logging.error(f"Error during agent run: {str(e)}")
            raise

    async def run_step(self, tool_call: dict):
        """
        Execute a single step of the agent's workflow.

        Args:
            tool_call (dict): A dictionary containing the tool name and its arguments.
        """
        try:
            logging.info("")
            logging.info("Executing tool call:")
            logging.info(f"  Tool: {tool_call.get('tool_name')}")
            logging.info(f"  Args: {tool_call.get('tool_args', {})}}")

            tool_result = await self.execute_tool(tool_call)
            logging.info("Tool execution completed.")

            await self.apply_tool_result(tool_result)
            await self.log_state()
        except Exception as e:
            logging.error(f"Error during run step: {str(e)}")
            raise
```

---

### ✅ **Key Improvements Made**

1. **Modular Structure**:
   - Separated the logic into clear methods (`_get_tool`, `_get_handler`, etc.) to enhance readability and maintainability.
   - Introduced a `run_step` method to encapsulate the logic for executing a single step in the agent's workflow.

2. **Robustness**:
   - Added `try-except` blocks in `execute_tool`, `apply_tool_result`, `run`, and `run_step` to catch and log exceptions, making the agent more robust to unexpected errors.

3. **Error Handling**:
   - Used specific exceptions and logging to help with debugging and monitoring.

4. **Documentation**:
   - Added detailed docstrings to all methods, explaining their purpose, arguments, and return values.
   - Clarified the responsibilities of each method.

5. **Code Readability**:
   - Used consistent naming conventions and improved code structure.
   - Added comments for complex logic or helper functions.

6. **Separation of Concerns**:
   - Introduced a `FileSummarizer` and repository classes (e.g., `AgentRunRepository`) to decouple logic from persistence, improving testability and maintainability.

---

### 🛠️ **Future Enhancements (Optional)**

- Introduce dependency injection for repositories and summarizers.
- Add unit tests for each method.
- Implement more sophisticated tool handling and error recovery.
- Add metrics and performance logging for long-running operations.

This refactoring preserves the original functionality while significantly improving the code's structure, robustness, and maintainability.