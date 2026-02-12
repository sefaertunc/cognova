"""Local embedding generation using MiniLM and UniXcoder.

Models (downloaded on first use, cached locally):
    - Text: sentence-transformers/all-MiniLM-L6-v2 (384 dims, ~80MB)
    - Code: microsoft/unixcoder-base-nine (768 dims, ~500MB)

Why dual embedding:
    Code embedding captures syntax/structure → finds similar framework patterns
    Text embedding captures intent/domain → finds similar business domains
    CEDAR combines both scores for retrieval ranking

No API calls. No cost. Runs on CPU.

Dependencies: sentence-transformers, torch (CPU)
"""


class EmbeddingGenerator:
    """Generate embeddings using local models.

    Methods:
        embed_text(text: str) -> list[float]  # MiniLM, 384 dims
        embed_code(code: str) -> list[float]  # UniXcoder, 768 dims
        embed_test(test: ApprovedTest) -> tuple[list[float], list[float]]  # both
    """

    pass
