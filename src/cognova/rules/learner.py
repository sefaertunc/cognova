"""Three-tier learning from feedback patterns.

Tier 1 — Immediate (threshold: 1):
    Auto-fix applied, counter incremented in learned_rules.json.
    Zero API cost.

Tier 2 — Threshold (threshold: >= 2):
    Pattern injected as prompt constraint for that framework/language.
    Constraints are appended to the generation prompt automatically.
    Zero API cost.

Tier 3 — MAPS (threshold: >= 10):
    Sonnet analyzes the pattern corpus → proposes permanent template update.
    Human must approve before the template is modified.
    API cost: ~1 Sonnet call per MAPS analysis.

Counter storage: .cognova/rules/learned_rules.json
"""


class RuleLearner:
    """Accumulate feedback patterns into rules.

    Methods:
        record_violation(rule_id: str, context: dict) -> None
        get_threshold_constraints(framework: str) -> list[str]
        check_maps_eligible() -> list[PatternCandidate]
        run_maps_analysis(candidate: PatternCandidate) -> MAPSSuggestion
    """

    pass
