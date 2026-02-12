"""Context-aware test repair loop.

Repair constraints:
    - Max 3 attempts per repair session
    - Max $0.50 cost per repair session
    - Whichever limit hits first stops the loop

Repair flow:
    1. Receive failure classification (must be STRUCTURAL)
    2. Collect: original scenario, generated code, error output, project context
    3. Send to LLM with repair-specific prompt (role: same as generation)
    4. Validate repaired code through rule engine
    5. Return repaired code or report failure after max attempts

Cost cap tracking:
    Each repair attempt logs cost via cost_tracker.
    Before attempt N, check: accumulated_repair_cost < $0.50
    If exceeded, stop and report to user.
"""


class TestRepairer:
    """Attempt to fix structural test failures.

    Methods:
        repair(
            scenario: Scenario,
            generated_code: str,
            failure: FailureClassification,
            context: TargetContext,
            quality: str = "standard"
        ) -> RepairResult

    RepairResult contains:
        - success: bool
        - code: str (repaired or original)
        - attempts: int
        - total_cost: float
        - history: list of attempt details
    """

    pass
