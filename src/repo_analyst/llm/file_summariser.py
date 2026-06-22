# src/repo_analyst/llm/file_summarizer.py

import logging
from time import time
from tracemalloc import start

from repo_analyst.llm.llm_client import LLMClient
from repo_analyst.logging import spinner
from repo_analyst.logging.spinner import Spinner


class FileSummarizer:

    def __init__(
        self,
        llm_client: LLMClient,
    ):
        self.llm_client = llm_client
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    async def summarize(
        self,
        file_path: str,
        content: str,
    ) -> str:
        start = time()
        spinner = Spinner(f"🧠 Local LLM summarizing file : {file_path}")

        spinner.start()
        prompt = f"""
You are analysing a source code file.

File:
{file_path}

Code:
{content}

Describe:

- Purpose of this file
- Main responsibilities
- Important classes/functions
- External integrations
- Architectural role

Keep the summary repository-specific.
Do not explain generic programming concepts.
Do not answer any user question.
"""
        summary = self.llm_client.generate(prompt)
        spinner.stop()
        duration = time() - start
        self.logger.info(f"✅ Summary completed in {duration:.1f}s")

        return summary
