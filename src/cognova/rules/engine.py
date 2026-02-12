"""Three-layer rule engine for test validation.

Layers (applied in order):
    1. Universal rules — apply to ALL frameworks (e.g., no empty test bodies,
       no hardcoded credentials, must have at least one assertion)
    2. Language rules — apply to specific languages (e.g., Python: no bare except,
       TypeScript: no any type in test assertions)
    3. Framework rules — apply to specific frameworks (e.g., pytest: use fixtures
       not setUp, Jest: use describe/it blocks)

Rule sources:
    - default_rules.json — shipped with Cognova, read-only
    - learned_rules.json — accumulated from feedback, project-specific

Validation output:
    - List of violations with severity (error/warning/info)
    - Auto-fixable violations are fixed in-place
    - Non-fixable violations are reported

Called by: mcp_server.py (generate_test pipeline, step 6 — after generation, before judge)
"""


class RuleEngine:
    """Load and apply validation rules.

    Methods:
        load_rules(framework: str, language: str) -> list[Rule]
        validate(code: str, framework: str, language: str) -> ValidationResult
        auto_fix(code: str, violations: list[Violation]) -> tuple[str, list[Violation]]
    """

    pass
