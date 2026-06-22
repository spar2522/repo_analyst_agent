from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
)
from sqlalchemy.sql import func

from sqlalchemy import ForeignKey

from repo_analyst.database.database import Base


class AgentRun(Base):

    __tablename__ = "agent_runs"

    id = Column(
        Integer,
        primary_key=True,
    )

    question = Column(
        Text,
        nullable=False,
    )

    repo_path = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )


class AgentFinding(Base):

    __tablename__ = "agent_findings"

    id = Column(
        Integer,
        primary_key=True,
    )

    run_id = Column(
        Integer,
        ForeignKey("agent_runs.id"),
        nullable=False,
    )

    file_path = Column(
        Text,
        nullable=False,
    )

    finding = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )


class FileSummary(Base):

    __tablename__ = "file_summaries"

    id = Column(
        Integer,
        primary_key=True,
    )

    repo_path = Column(
        Text,
        nullable=False,
    )

    file_path = Column(
        Text,
        nullable=False,
    )

    summary = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )
