from ai_provider import AI
from repo_analyst.logging.spinner import Spinner


class AnswerGenerator:

    def __init__(
        self,
        ai: AI,
    ):
        self.ai = ai

    async def generate(
        self,
        question: str,
        findings: list[str],
    ) -> str:

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

        spinner = Spinner(f"🧠 Local LLM Finalising answer .....  ")
        spinner.start()

        answer = await self.ai.generate(prompt)
        spinner.stop()
        return answer
