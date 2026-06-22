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

    def summarize(
        self,
        question: str,
        file_path: str,
        content: str,
    ) -> str:
        start = time()
        spinner = Spinner(f"🧠 Local LLM summarizing file : {file_path}")

        spinner.start()
        prompt = f"""
You are helping answer a repository question.

Question:
{question}

File:
{file_path}

Code:
{content[:4000]}  # Limit content to first 4000 characters for summarization

Instructions:

Summarize only information relevant to answering the question.

If the file is not relevant, explicitly say so.

Return 2-5 concise bullet points.
"""
        summary = self.llm_client.generate(prompt)
        spinner.stop()
        duration = time() - start
        self.logger.info(f"✅ Summary completed in {duration:.1f}s")

        return summary
