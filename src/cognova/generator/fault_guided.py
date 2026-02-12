"""Fault-guided test generation (v1.2 feature, ACH pattern).

Uses Analysis of Competing Hypotheses (ACH) pattern:
    1. Sonnet generates hypotheses about potential faults in target code
    2. For each hypothesis, generate a test that would detect that fault
    3. Tests are designed to discriminate between hypotheses

This is NOT mutation testing (we don't mutate code). Instead:
    - Analyze the code structure
    - Hypothesize what could go wrong
    - Generate tests that would catch those faults

Separate MCP tool, separate cost from main generation.
Model: Sonnet for hypothesis generation, quality tier for test generation.

Called by: mcp_server.py (generate_fault_tests tool)
"""


class FaultGuidedGenerator:
    """Generate tests guided by fault hypothesis analysis.

    Methods:
        generate_hypotheses(target: TargetContext) -> list[FaultHypothesis]
        generate_test_for_hypothesis(
            hypothesis: FaultHypothesis,
            scenario: Scenario,
            context: TargetContext,
            quality: str
        ) -> GenerationResult
    """

    pass
