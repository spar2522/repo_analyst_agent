from dataclasses import dataclass, field


@dataclass
class AgentState:
    """Represents the state of an agent during repository analysis."""

    question: str
    """The question or task the agent is currently addressing."""

    files_seen: set[str] = field(default_factory=set)
    """Set of files that the agent has encountered in the repository."""

    files_read: set[str] = field(default_factory=set)
    """Set of files that the agent has read or processed."""

    observations: list[str] = field(default_factory=list)
    """List of observations or notes made by the agent during analysis."""