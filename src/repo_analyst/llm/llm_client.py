from ai_provider import AI
from ai_provider.config import AIProviderConfig
from ai_provider.generation_request import GenerationRequest
from ai_provider.provider_type import Provider
import requests


class LLMClient:

    def __init__(
        self,
        model: str = "qwen3:14b",
        base_url: str = "http://localhost:11434",
    ) -> None:

        self.model = model
        self.base_url = base_url

        config = AIProviderConfig(
            provider=Provider.OLLAMA,
            model=model,
            base_url=base_url,
        )

        self._provider = AI.create(config)

    async def generate(self, prompt: str) -> str:
        """
        Generate a response from the language model.

        Args:
            prompt: The input prompt to send to the model.

        Returns:
            The generated response text.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
            ValueError: If the response contains an error message.
        """
        response = await self._provider.generate(
            GenerationRequest(
                prompt=prompt,
            )
        )
        return response