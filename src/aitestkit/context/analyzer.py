"""Orchestrates project context analysis.

Flow:
    1. Scan project files by configured languages
    2. Parse each file via tree-sitter (parser.py)
    3. Build dependency graph (graph.py)
    4. Compute structural hashes (hasher.py)
    5. Compare hashes to stored values → skip unchanged files
    6. Send changed structural data to Sonnet for summary
    7. Store summary + embeddings in LanceDB

Called by: mcp_server.py (init_project tool, auto-init on first generate_test)
Depends on: parser.py, graph.py, hasher.py, memory/lancedb_store.py
Model call: Sonnet (analysis role) — generates natural language project summary
"""


class ProjectAnalyzer:
    """Main orchestrator for project context analysis.

    Attributes:
        project_path: Root path of the user's project
        config: AITestKit config from .aitestkit/config.yaml
        parser: TreeSitterParser instance
        graph: DependencyGraph instance
        hasher: StructuralHasher instance
        store: LanceDBStore instance

    Methods:
        analyze() -> ProjectContext: Full analysis, stores results
        analyze_incremental() -> ProjectContext: Only re-analyze changed files
        get_context_for_target(target_path: str) -> TargetContext:
            Walk dependency graph from target, return relevant signatures + imports
    """

    pass
