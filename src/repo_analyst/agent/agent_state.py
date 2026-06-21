from dataclass import dataclass, field


@dataclass
class AgentState:
    """Represents the state of an agent during repository analysis."""

    question: str
    """The question or task the agent is currently addressing."""

    repo_path: str
    """Path to the repository being analyzed."""

    files_seen: set[str] = field(default_factory=set)
    """Set of files that the agent has encountered in the repository."""

    search_results: set[str] = field(default_factory=set)
    """Set of files or content that the agent has found via search."""

    files_read: set[str] = field(default_factory=set)
    """Set of files that the agent has read or processed."""

    observations: list[str] = field(default_factory=list)
    """List of observations or notes made by the agent during analysis."""

    def summary(self):
        """Returns a summary of the agent's state with counts of key elements."""
        return {
            "files_seen": len(self.files_seen),
            "files_read": len(self.files_read),
            "search_results": len(self.search_results),
            "observations": len(self.observations),
        }

    def __repr__(self):
        return (
            f"AgentState(question='{self.question}', repo_path='{self.repo_path}', "
            f"files_seen={len(self.files_seen)}, files_read={len(self.files_read)}, "
            f"search_results={len(self.search_results)}, observations={len(self.observations)})"
        )