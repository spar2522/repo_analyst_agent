from repo_analyst.llm.embeddings_client import (
    EmbeddingClient,
)

"""Test script for EmbeddingClient.

This script demonstrates generating an embedding using the EmbeddingClient and prints the length of the resulting embedding vector.
"""

# Initialize the embedding client
client = EmbeddingClient()

# Generate an embedding for the test text
TEST_TEXT = "Webhooks receive GitHub events"
embedding = client.generate_embedding(TEST_TEXT)

# Print the length of the embedding vector
print(len(embedding))