from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from repo_analyst.database.database import Base


class AgentRun(Base):
    """Represents a run of an analysis agent."""

    __tablename__ = "agent_runs"

    id = Column(
        Integer,
        primary_key=True,
        doc="Unique identifier for the agent run",
    )

    question = Column(
        Text,
        nullable=False,
        doc="The question or task that the agent was asked to analyze",
    )

    repo_path = Column(
        Text,
        nullable=False,
        doc="The file system path to the repository being analyzed",
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        doc="Timestamp when the agent run was created",
    )

    # Relationship to findings
    findings = relationship("AgentFinding", back_populates="run")


class AgentFinding(Base):
    """Represents a finding discovered during an agent run."""

    __tablename__ = "agent_findings"

    id = Column(
        Integer,
        primary_key=True,
        doc="Unique identifier for the finding",
    )

    run_id = Column(
        Integer,
        ForeignKey("agent_runs.id"),
        nullable=False,
        doc="Reference to the agent run that discovered this finding",
    )

    file_path = Column(
        Text,
        nullable=False,
        doc="The file system path to the file where the finding was discovered",
    )

    finding = Column(
        Text,
        nullable=False,
        doc="The specific finding or issue discovered in the file",
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        doc="Timestamp when the finding was recorded",
    )

    # Relationship to agent run
    run = relationship("AgentRun", back_populates="findings")

    __table_args__ = (
        # Index on run_id for faster lookups when querying by run
        # Index on created_at for time-based filtering
        # Index on file_path for searching findings by file
        # Index on finding for full-text search capabilities
        # These are optional and can be adjusted based on query patterns
        # Uncomment the ones relevant to your use case
        # Index("idx_run_id", "run_id"),
        # Index("idx_created_at", "created_at"),
        # Index("idx_file_path", "file_path"),
        # Index("idx_finding", "finding"),
    )