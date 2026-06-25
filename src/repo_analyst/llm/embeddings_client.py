import requests


class EmbeddingClient:

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:

        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": text,
            },
        )

        response.raise_for_status()

        return response.json()["embedding"]
