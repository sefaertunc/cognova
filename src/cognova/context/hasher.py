"""Structural hashing for incremental analysis.

Hash ONLY function/class signatures:
    - Function names, parameter names, parameter types, return types
    - Class names, base classes, method signatures

Hash does NOT include:
    - Function/method bodies
    - Comments, docstrings
    - Formatting, whitespace
    - Variable assignments inside functions

Purpose: If hash unchanged since last analysis, skip re-embedding.
Only signature-level changes trigger re-analysis.
"""


class StructuralHasher:
    """Compute and compare structural hashes.

    Methods:
        hash_file(structure: FileStructure) -> str
        has_changed(path: Path, new_hash: str) -> bool
        update_stored_hash(path: Path, new_hash: str) -> None
        load_stored_hashes() -> dict[str, str]
    """

    pass
