"""Prompt regression testing with cost delta check.

When a prompt template changes, validates that output quality doesn't degrade.

Flow (Pipeline 7):
    1. Load golden set (approved scenarios with known-good outputs from LanceDB)
    2. Re-generate tests using NEW template for each golden scenario
    3. LLM-as-Judge (Haiku) scores both old and new outputs
    4. Compare scores: regression = new_score < old_score - threshold
    5. Compare costs: warn if new_avg_cost > old_avg_cost * 1.15
    6. Return report

In v3.2 this was split into comparator/runner/scorer.
In v4.0 it's a single module — the pipeline is orchestrated here.

Called by: mcp_server.py (validate_prompt_change tool, Pipeline 7)
Models: quality tier for generation, Haiku for judge
"""


class PromptRegressionTester:
    """Test prompt template changes against golden set.

    Methods:
        validate(
            template_path: str,
            golden_set_size: int = 10
        ) -> RegressionReport

    RegressionReport contains:
        - passed: int
        - regressed: int
        - improved: int
        - cost_delta_pct: float
        - cost_warning: bool (True if delta > 15%)
        - details: list[ScenarioComparison]
    """

    pass
