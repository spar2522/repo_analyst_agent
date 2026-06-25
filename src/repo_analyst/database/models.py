from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
    JSON,
    ForeignKey,
)
from sqlalchemy.sql import func

from repo_analyst.database.database import Base


class AgentRun(Base):
    """Represents a run of an agent with a specific question and repository."""
    __tablename__ = "agent_runs"

    id = Column(
        Integer,
        primary_key=True,
    )

    question = Column(
        Text,
        nullable=False,
        doc="The question posed to the agent during this run.",
    )

    repo_path = Column(
        Text,
        nullable=False,
        doc="The path to the repository being analyzed.",
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        doc="Timestamp when this agent run was created.",
    )


class AgentFinding(Base):
    """Stores findings discovered by an agent during a specific run."""
    __tablename__ = "agent_findings"

    id = Column(
        Integer,
        primary_key=True,
    )

    run_id = Column(
        Integer,
        ForeignKey("agent_runs.id"),
        nullable=False,
        doc="Reference to the agent run that discovered this finding.",
    )

    file_path = Column(
        Text,
        nullable=False,
        doc="The path to the file where this finding was discovered.",
    )

    finding = Column(
        Text,
        nullable=False,
        doc="The specific finding discovered by the agent.",
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        doc="Timestamp when this finding was recorded.",
    )


class FileSummary(Base):
    """Stores a summary of the content of a specific file."""
    __tablename__ = "file_summaries"

    id = Column(
        Integer,
        primary_key=True,
    )

    repo_path = Column(
        Text,
        nullable=False,
        doc="The path to the repository containing this file.",
    )

    file_path = Column(
        Text,
        nullable=False,
        doc="The path to the file being summarized.",
    )

    summary = Column(
        Text,
        nullable=False,
        doc="A summary of the content of the file.",
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        doc="Timestamp when this summary was created.",
    )


class FileEmbedding(Base):
    """Stores the embedding vector for a specific file."""
    __tablename__ = "file_embeddings"

    id = Column(
        Integer,
        primary_key=True,
    )

    repo_path = Column(
        Text,
        nullable=False,
        doc="The path to the repository containing this file.",
    )

    file_path = Column(
        Text,
        nullable=False,
        doc="The path to the file for which the embedding was generated.",
    )

    embedding = Column(
        JSON,
        nullable=False,
        doc="The embedding vector representing the file's content.",
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        doc="Timestamp when this embedding was created.",
    )