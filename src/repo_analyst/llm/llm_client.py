import requests
from typing import Optional


class LLMClient:
    """Client for interacting with a language model API."""

    def __init__(
        self,
        model: str = "qwen3:14b",
        base_url: str = "http://localhost:11434",
    ) -> None:
        """
        Initialize the LLM client.

        Args:
            model: The model name to use for API requests.
            base_url: The base URL for the API endpoint.
        """
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str) -> str:
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
        try:
            response = self._send_request(prompt)
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            raise e
        except ValueError as e:
            raise e

    def _send_request(self, prompt: str) -> requests.Response:
        """
        Send a request to the language model API.

        Args:
            prompt: The input prompt to send to the model.

        Returns:
            The HTTP response object from the API.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=300,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise e

        return response
