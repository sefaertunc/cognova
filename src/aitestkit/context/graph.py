"""Dependency graph construction from parsed file structures.

Given parsed files, builds a directed graph where:
    - Nodes = files (or classes/functions within files)
    - Edges = import/dependency relationships

Used by:
    - ProjectAnalyzer.get_context_for_target(): walk graph from target file
      to collect all directly-referenced signatures for prompt context injection.
"""


class DependencyGraph:
    """Build and query dependency relationships.

    Methods:
        build(files: list[FileStructure]) -> None
        get_dependencies(target: str, depth: int = 2) -> list[FileStructure]
        get_dependents(target: str) -> list[str]
        to_dict() -> dict: Serializable representation
    """

    pass
