import logging
from time import time

from repo_analyst.llm.llm_client import LLMClient
from repo_analyst.logging.spinner import Spinner


class FileSummarizer:
    """Generates structured technical summaries of source code files for AI knowledge repositories."""

    def __init__(self, llm_client: LLMClient):
        """
        Initialize the file summarizer.

        Args:
            llm_client: Language model client for generating summaries
        """
        self.llm_client = llm_client
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    async def summarize(self, file_path: str, content: str) -> str:
        """
        Generate a structured technical summary of a source code file.

        The summary includes specific technical metadata in a standardized format
        for use in AI knowledge repositories and semantic retrieval systems.

        Args:
            file_path: Path to the file being summarized
            content: Full content of the file to be analyzed

        Returns:
            Structured summary containing:
            - Purpose of the file
            - Key classes and functions
            - Input/output requirements
            - Dependencies and integrations
            - Architectural context

        Raises:
            Exception: If summary generation fails
        """
        start_time = time()
        spinner = Spinner(f"🧠 Local LLM summarizing file: {file_path}")

        try:
            spinner.start()
            prompt = self._construct_llm_prompt(file_path, content)
            summary = self.llm_client.generate(prompt)
            spinner.stop()
            duration = time() - start_time
            self.logger.info(f"✅ Summary completed in {duration:.1f}s")

            return summary
        except Exception as e:
            spinner.stop()
            self.logger.error(f"❌ Error summarizing file {file_path}: {str(e)}")
            raise

    def _construct_llm_prompt(self, file_path: str, content: str) -> str:
        """Construct the prompt for the language model with standardized instructions."""
        return f"""
File:
{file_path}

Code:
{content}

You are creating repository knowledge for another AI agent.

Your output will later be embedded and used for semantic retrieval.

Do NOT write a human-friendly summary.

Instead extract the important technical knowledge.

Return exactly the following sections:

Purpose:
- What problem does this file solve?

Classes:
- List important classes.

Functions:
- List important public functions.

Inputs:
- What inputs does this file receive?

Outputs:
- What does this file produce or return?

Dependencies:
- Important libraries, frameworks or services used.

Collaborates With:
- Other repository files, modules or components this file directly interacts with.

External Systems:
- GitHub
- Redis
- PostgreSQL
- Ollama
- FastAPI
- Docker
(only include the ones actually used)

Important Concepts:
- List important concepts discussed in this file.
Examples:
Webhook
Authentication
Repository Indexing
Embeddings
Background Worker
Prompt Engineering

Keywords:
List 10-20 important keywords and identifiers exactly as they appear in the code.
Include:
- class names
- function names
- constants
- filenames
- environment variables
- API routes
- important symbols

Architectural Role:
Describe how this file fits into the overall repository.
"""