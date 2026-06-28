from repo_analyst.llm.llm_client import LLMClient
from repo_analyst.logging.spinner import Spinner


class AnswerGenerator:
    """Generates repository analysis answers using an LLM based on provided findings."""

    def __init__(
        self,
        llm_client: LLMClient,
    ):
        """Initialize answer generator with an LLM client.

        Args:
            llm_client: Client for interacting with the language model
        """
        self.llm_client = llm_client

    def generate(
        self,
        question: str,
        findings: list[str],
    ) -> str:
        """Generate an answer to the given question using repository findings.

        Args:
            question: The question to answer
            findings: List of repository analysis findings to use as context

        Returns:
            The generated answer based on the findings
        """
        if not findings:
            return "No findings provided to generate an answer."

        findings_text = "\n\n".join(findings)

        prompt = f"""
You are analysing a software repository.

Question:
{question}

Repository Findings:
{findings_text}

Instructions:

- Answer ONLY using the repository findings.
- Do NOT provide generic software engineering explanations.
- Do NOT explain concepts unless they are mentioned in the findings.
- Focus on how this repository implements the concept.
- If the findings do not contain enough information, explicitly say so.
- Reference filenames when relevant.
- Be specific and concrete.

Answer:
"""

        spinner = Spinner("🧠 Local LLM Finalising answer...")
        spinner.start()

        try:
            answer = self.llm_client.generate(prompt)
        finally:
            spinner.stop()

        return answer