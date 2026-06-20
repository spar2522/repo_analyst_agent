from dataclass import dataclass, field


@dataclass
class AgentState:
    """Represents the state of an agent during repository analysis."""

    question: str
    """The question or task the agent is currently addressing."""

    repo_path: str
    """The path to the repository being analyzed."""

    files_seen: set[str] = field(default_factory=set)
    """Set of files that the agent has encountered in the repository."""

    search_results: set[str] = field(default_factory=set)
    """Set of search results or relevant files identified by the agent."""

    files_read: set[str] = field(default_factory=set)
    """Set of files that the agent has read or processed."""

    observations: list[str] = field(default_factory=list)
    """List of observations or notes made by the agent during analysis."""

    def print_state(self):
        """Prints the current state of the agent for debugging and tracking purposes."""
        print()
        print("STATE")
        print("-" * 40)

        print(f"Files Seen: {len(self.files_seen)}")
        print(f"Files Read: {len(self.files_read)}")

        print()

        print("Recent Observations:")

        for observation in self.observations[-5:]:
            print(f"  - {observation}")