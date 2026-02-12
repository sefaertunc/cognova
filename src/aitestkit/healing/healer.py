"""Self-healing suggest mode (default).

When an existing approved test starts failing after a code change:
    1. Classify failure (structural vs assertion)
    2. Diff the code-under-test (what changed since test was approved)
    3. Generate fix suggestion with explanation
    4. Present to user for approval
    5. If approved: update test, keep in LanceDB
    6. If rejected: user fixes manually

Tagged tests:
    Healed tests are tagged with metadata: { healed: true, healed_at: timestamp }
    Healed tests are EXCLUDED from LanceDB few-shot retrieval until re-approved.
    This prevents potentially degraded tests from influencing new generation.

Self-healing modes (configured in .aitestkit/config.yaml):
    off — No healing suggestions
    suggest — (DEFAULT) Present fix, require human approval
    auto — Auto-apply cosmetic fixes only (see auto_healer.py)
"""


class TestHealer:
    """Generate healing suggestions for broken tests.

    Methods:
        diagnose(test_path: str, failure_output: str) -> HealingDiagnosis
        suggest_fix(diagnosis: HealingDiagnosis) -> HealingSuggestion
        apply_fix(suggestion: HealingSuggestion) -> HealingResult
    """

    pass
