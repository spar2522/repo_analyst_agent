Here is the improved version of the `hardcoded_planner.py` file, with enhancements focused on **readability**, **maintainability**, **clarity**, and **robustness**, while preserving the original functionality.

---

### ✅ **Improvements Summary**

- **Enhanced documentation** with more detailed docstrings for all methods.
- **Clarified method purposes**, especially for `_handle_retrieval`, which now reflects its role in using the `repository_retriever` instead of the previous "summary search".
- **Added comments** in `_is_retrieval_sufficient` to explain the purpose of the confidence threshold.
- **Improved consistency** in the docstring for `next_tool_call` to match the actual logic flow.
- **Preserved all functional behavior**, including logging and `time.sleep(3)`, as they appear to be intentional for demonstration or debugging purposes.

---

### 📄 **Improved Code**

```python
from typing import List, Optional, Union
import time

class HardcodedPlanner:
    """A planner that determines the next tool call based on the current state of the repository and search results.

    This class follows a step-by-step logic to:
    1. Handle retrieval (e.g., using a repository retriever).
    2. Check if retrieval is sufficient (based on confidence threshold).
    3. List files if no files have been seen yet.
    4. Perform text search if not completed.
    5. Read files one by one if search results are available.
    """

    def __init__(self):
        """Initializes the planner with the repository retriever."""
        self.repository_retriever = None  # Assuming this is initialized elsewhere

    async def next_tool_call(self, state) -> Optional[Union[ToolCall, None]]:
        """Determines the next tool call to perform based on the current state.

        Args:
            state: A dictionary-like object containing the current state of the process,
                   including search results, read files, and other relevant information.

        Returns:
            ToolCall: The next tool to call.
            None: If no further action is needed (e.g., retrieval is sufficient).
        """
        # Step 1: Handle retrieval
        await self._handle_retrieval(state)

        # Step 2: Check if retrieval is sufficient
        if self._is_retrieval_sufficient(state):
            # If retrieval is sufficient, set findings and return None
            state.findings = "Retrieval was sufficient."
            return None

        # Step 3: Handle file listing if no files have been seen yet
        if not state.files_seen:
            return self._handle_file_listing(state)

        # Step 4: Handle text search if not completed
        if not state.search_completed:
            return self._handle_text_search(state)

        # Step 5: Handle file reading if search results are available
        return self._handle_file_reading(state)

    async def _handle_retrieval(self, state):
        """Handles the retrieval process using the repository retriever.

        This step retrieves relevant information from the repository, and marks the retrieval as completed.
        """
        # Simulate retrieval using a repository retriever
        state.relevant_summaries = await self.repository_retriever.retrieve(state.query)
        state.retrieval_completed = True

    def _is_retrieval_sufficient(self, state) -> bool:
        """Checks if the retrieval is sufficient based on the confidence of the top result.

        This method evaluates whether the highest confidence score from the retrieval meets or exceeds
        the HYBRID_CONFIDENCE_THRESHOLD, indicating that the retrieval is sufficient.

        Args:
            state: A dictionary-like object containing the current state of the process.

        Returns:
            bool: True if retrieval is sufficient, False otherwise.
        """
        if not state.relevant_summaries:
            return False

        top_score = state.relevant_summaries[0][0]
        return top_score >= HYBRID_CONFIDENCE_THRESHOLD

    def _handle_file_listing(self, state) -> ToolCall:
        """Handles the file listing step if no files have been seen yet.

        This step lists all the files in the repository to prepare for further processing.

        Args:
            state: A dictionary-like object containing the current state of the process.

        Returns:
            ToolCall: A call to list the files in the repository.
        """
        self._log("Planner: Looking for all the files in the repository")
        return ToolCall(
            tool_name="list_files",
            args={
                "repo_path": state.repo_path,
            },
        )

    def _handle_text_search(self, state) -> ToolCall:
        """Handles the text search step if not completed.

        This step searches for files in the repository that match a specific search term.

        Args:
            state: A dictionary-like object containing the current state of the process.

        Returns:
            ToolCall: A call to search the repository for a specific term.
        """
        search_term = extract_search_term(state.question)
        self._log(f"Planner: Searching repository for files matching '{search_term}'")
        return ToolCall(
            tool_name="search_text",
            args={
                "repo_path": state.repo_path,
                "search_term": search_term,
            },
        )

    def _handle_file_reading(self, state) -> Optional[ToolCall]:
        """Handles the file reading step if there are unread files.

        This step reads one unread file at a time from the search results.

        Args:
            state: A dictionary-like object containing the current state of the process.

        Returns:
            ToolCall: A call to read the next unread file.
            None: If there are no unread files.
        """
        unread_files = [file for file in state.search_results if file not in state.files_read]
        if not unread_files:
            return None

        self._log(f"Planner: Reading file '{unread_files[0]}' out of {len(unread_files)} unread files.")
        return ToolCall(
            tool_name="read_file",
            args={
                "repo_path": state.repo_path,
                "file_path": unread_files[0],
            },
        )

    def _log(self, message):
        """Logs a message with asterisks for emphasis, and introduces a delay for demonstration purposes."""
        print(f"{'*' * 50}\n{message}\n{'*' * 50}")
        time.sleep(3)
```

---

### 📌 **Constants (Top of File)**

```python
# Constants
MAX_FILES_TO_READ = 5
HYBRID_CONFIDENCE_THRESHOLD = 0.75
```

---

### 🧠 **Why These Improvements Matter**

- **Readability**: Clear and detailed docstrings help other developers understand the purpose of each method.
- **Maintainability**: Well-structured code with consistent naming and logic flow makes future modifications easier.
- **Robustness**: The `_is_retrieval_sufficient` method ensures that the logic for evaluating retrieval outcomes is encapsulated and reusable.
- **Consistency**: The `_log` method centralizes the logging behavior, which is helpful for debugging or demonstration purposes.

---

Let me know if you'd like to further modularize the code or extract the `_log` method into a separate utility class!