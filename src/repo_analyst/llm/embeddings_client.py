import requests
from typing import Optional, List
from requests.exceptions import RequestException, JSONDecodeError


class EmbeddingClient:
    """Client for generating text embeddings using a remote API."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "nomic-embed-text",
        timeout: float = 10.0,
    ) -> None:
        """
        Initialize the EmbeddingClient.

        Args:
            base_url: Base URL for the embeddings API (default: localhost:11434)
            model: Name of the embedding model to use (default: nomic-embed-text)
            timeout: Request timeout in seconds (default: 10.0)
        """
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    def generate_embedding(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate an embedding for the given text.

        Args:
            text: Input text to embed

        Returns:
            List of floats representing the embedding vector

        Raises:
            RequestException: If the API request fails
            KeyError: If the response is missing the embedding field
            JSONDecodeError: If the response is not valid JSON
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            
            if "embedding" not in data:
                raise KeyError(f"Response missing required 'embedding' field: {data}")
                
            return data["embedding"]

        except RequestException as e:
            raise RequestException(f"API request failed: {str(e)}") from e
        except JSONDecodeError as e:
            raise JSONDecodeError(f"Invalid JSON response: {str(e)}") from e