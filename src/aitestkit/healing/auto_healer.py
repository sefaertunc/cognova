"""Self-healing auto mode — cosmetic fixes only.

Auto-apply criteria (ALL must be true):
    - config.self_healing.mode == "auto"
    - Failure is STRUCTURAL (not assertion)
    - Fix is COSMETIC: renames, import path changes, type annotation updates
    - Fix does NOT change test assertions or expected values

Behavioral changes ALWAYS require human approval regardless of mode:
    - Changed expected values
    - Added/removed assertions
    - Modified test logic
    - Changed mock behavior

This distinction prevents self-healing from silently accepting bugs
in the code-under-test by weakening test assertions.
"""


class AutoHealer:
    """Auto-apply cosmetic fixes without human approval.

    Methods:
        is_cosmetic(original: str, fixed: str) -> bool
        auto_heal(test_path: str, failure_output: str) -> AutoHealResult
    """

    pass
