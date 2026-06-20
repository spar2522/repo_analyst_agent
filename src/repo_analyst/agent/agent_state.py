from dataclasses import dataclass, field


@dataclass
class AgentState:
    """Represents the state of an agent during repository analysis."""

    question: str
    """The question or task the agent is currently addressing."""

    repo_path: str
    """The file system path to the repository being analyzed."""

    files_seen: set[str] = field(default_factory=set)
    """Set of files that the agent has encountered in the repository.
    
    This includes all files that have been referenced or considered
    during the analysis process, whether or not they have been read.
    """

    search_results: set[str] = field(default_factory=set)
    """Set of files that matched the agent's search criteria during analysis."""

    files_read: set[str] = field(default_factory=set)
    """Set of files that the agent has read or processed.
    
    This includes files that have been fully analyzed or examined
    for content relevant to the current task.
    """

    observations: list[str] = field(default_factory=list)
    """List of observations or notes made by the agent during analysis.
    
    This may include code patterns, potential issues, or other
    relevant information discovered in the repository.
    """