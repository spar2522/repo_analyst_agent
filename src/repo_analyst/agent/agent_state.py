from dataclasses import dataclass, field


@dataclass
class AgentState:

    question: str

    files_seen: set[str] = field(default_factory=set)

    files_read: set[str] = field(default_factory=set)

    observations: list[str] = field(default_factory=list)
