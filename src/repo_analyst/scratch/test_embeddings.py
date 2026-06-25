from repo_analyst.llm.embeddings_client import (
    EmbeddingClient,
)

client = EmbeddingClient()

embedding = client.generate_embedding("Webhooks receive GitHub events")

print(len(embedding))
