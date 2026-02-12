"""Individual rule definitions and matching logic.

Each rule has:
    - id: Unique identifier (e.g., "UNIV-001", "PY-003", "PYTEST-007")
    - layer: "universal" | "language" | "framework"
    - severity: "error" | "warning" | "info"
    - pattern: Regex or AST pattern to match
    - message: Human-readable description
    - auto_fix: Optional fix function (returns corrected code)
    - counter: Number of times this rule was triggered (for learning)
"""


class Rule:
    """Single validation rule."""

    pass


class ValidationResult:
    """Result of rule validation.

    Attributes:
        passed: bool
        violations: list[Violation]
        auto_fixed: list[Violation]  # violations that were auto-corrected
        code: str  # potentially auto-fixed code
    """

    pass
