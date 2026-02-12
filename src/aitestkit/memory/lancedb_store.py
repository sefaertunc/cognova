"""LanceDB vector storage for approved test patterns.

Uses LanceDB OSS (open-source, Apache 2.0, local files).
NOT LanceDB Cloud (SaaS). Zero cost, no network calls.

Storage location: .aitestkit/memory/
Each approved test gets TWO vectors:
    - Code embedding (UniXcoder): captures syntax/structure
    - Text embedding (MiniLM): captures intent/domain

Source of truth: test files on disk + feedback logs.
LanceDB is ALWAYS rebuildable from source of truth via manage_memory(action="rebuild").

Healed tests are stored but tagged { healed: true }.
Healed tests are excluded from few-shot retrieval until re-approved.

Dependencies: lancedb, pyarrow
"""


class LanceDBStore:
    """Local vector database for test pattern storage.

    Methods:
        init_store(path: Path) -> None
        store_test(test: ApprovedTest, code_embedding: list[float], text_embedding: list[float]) -> None
        remove_test(test_id: str) -> None
        search_similar(query_embedding: list[float], embedding_type: str, top_k: int = 5) -> list[SearchResult]
        rebuild_from_source(approved_dir: Path, feedback_dir: Path) -> RebuildStats
        get_stats() -> StoreStats
        list_entries(query: str | None = None) -> list[EntryInfo]
    """

    pass
