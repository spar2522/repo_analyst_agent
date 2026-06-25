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

    repository = FileEmbeddingRepository()

    embeddings = await repository.get_all_embeddings(REPO_PATH)

    client = EmbeddingClient()

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
    question_embedding = client.generate_embedding(QUESTIONS["redis"])

    search = EmbeddingSearch()

    results = search.search(
        question_embedding=question_embedding,
        embeddings=embeddings,
    )

    for score, embedding in results:

        print(f"{score:.3f} | {embedding.file_path}")


asyncio.run(main())
