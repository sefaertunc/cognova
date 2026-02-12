"""Per-operation cost tracking with precise token accounting.

CRITICAL: Logs EVERY API call regardless of outcome.
Rejected generations, failed repairs, unapproved heals — ALL logged.

Each log entry contains:
    - tool: which MCP tool triggered this (e.g., "generate_test")
    - scenario: scenario file path (if applicable)
    - step: pipeline step name (e.g., "scot_reasoning", "code_generation", "judge")
    - role: model role used (e.g., "generation", "analysis", "validation")
    - model: actual model string used (e.g., "claude-sonnet-4-5-20250514")
    - input_tokens: exact count from API response
    - output_tokens: exact count from API response
    - cost_usd: calculated from pricing registry
    - outcome: "approved" | "rejected" | "failed" | "repaired" | "pending"
    - timestamp: ISO 8601

Storage: .aitestkit/costs/YYYY-MM-DD.jsonl (one file per day, append-only)

Pricing registry:
    Keyed by model string, not role. Supports multi-provider pricing.
    Users manage their own API keys — precise logging is essential.

get_cost_summary output includes breakdown by outcome:
    Total: $1.24 (18 operations)
    ├── Approved generations: $0.68 (6 tests)
    ├── Rejected generations: $0.22 (2 tests)
    ├── Repair attempts: $0.28 (5 attempts)
    └── Other (judge, SCoT, analysis): $0.06
"""

PRICING_REGISTRY: dict[str, dict[str, float]] = {
    # Anthropic models (February 2026)
    "claude-opus-4-6": {"input": 5.0, "output": 25.0},
    "claude-opus-4-5-20250514": {"input": 5.0, "output": 25.0},
    "claude-sonnet-4-5-20250514": {"input": 3.0, "output": 15.0},
    "claude-haiku-4-5-20250514": {"input": 1.0, "output": 5.0},
}


class CostTracker:
    """Track and report API costs per operation.

    Methods:
        log_operation(entry: CostEntry) -> None
        get_summary(period: str = "today") -> CostSummary
        get_repair_session_cost(session_id: str) -> float
        export_csv(path: Path, period: str = "all") -> None
    """

    pass


class CostEntry:
    """Single cost log entry.

    Attributes:
        tool: str
        scenario: str | None
        step: str
        role: str
        model: str  # actual model string, not role name
        input_tokens: int
        output_tokens: int
        cost_usd: float
        outcome: str
        timestamp: datetime
    """

    pass
