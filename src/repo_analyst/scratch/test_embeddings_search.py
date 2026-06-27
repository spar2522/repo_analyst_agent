import asyncio

from repo_analyst.database.file_embedding_repository import (
    FileEmbeddingRepository,
)

from repo_analyst.llm.embeddings_client import (
    EmbeddingClient,
)

from repo_analyst.search.embeddings_search import (
    EmbeddingSearch,
)

REPO_PATH = "/Users/arpitratan/ai-lab/ai_autodoc"


async def main():
    """Main function to execute the embeddings search test.

    This function initializes the necessary components, generates an embedding
    for a test question, and performs a search using the EmbeddingSearch class.
    """

    # Initialize the file embedding repository
    repository = FileEmbeddingRepository()

    # Retrieve all embeddings for the specified repository path
    embeddings = await repository.get_all_embeddings(REPO_PATH)

    # Initialize the embedding client
    client = EmbeddingClient()

    # Define test questions for the search
    QUESTIONS = {
        "webhook": "Why are webhooks used?",
        "redis": "How is Redis used in this repository?",
        "worker": "How are background workers implemented?",
        "github": "How does GitHub integration work?",
        "review": "How does AutoDoc review code?",
        "pr": "How are pull requests created?",
        "queue": "How are tasks queued and processed?",
        "api": "How is FastAPI used in this project?",
        "architecture": "Explain the architecture of this repository.",
        "flow": "What happens when code is pushed to GitHub?",
        "entrypoint": "What are the main entry points of this application?",
        "storage": "How is data persisted in the system?",
    }

    # Generate an embedding for the selected test question
    question_embedding = client.generate_embedding(QUESTIONS["worker"])

    # Initialize the embedding search component
    embedding_search = EmbeddingSearch()

    # Perform the search using the generated embedding and retrieved embeddings
    results = embedding_search.search(
        question_embedding=question_embedding,
        embeddings=embeddings,
    )

    # Print the search results with scores and corresponding file paths
    for score, embedding in results:
        print(f"{score:.3f} | {embedding.file_path}")


if __name__ == "__main__":
    asyncio.run(main())
