"""Criterion definitions and framework-specific criteria registry.

Data classes for the rubric system:
- Criterion: Single yes/no question for Haiku (id, category, question, hard_fail)
- CriterionResult: Haiku's answer to a criterion (passed, reasoning)
- Category: Enum of 4 criterion categories

Framework criteria registry:
- FRAMEWORK_CRITERIA: dict mapping framework name → list of Criterion
- GENERIC_FRAMEWORK_CRITERIA: fallback for unknown frameworks
- get_framework_criteria(framework): lookup with generic fallback

Categories:
  A: scenario_alignment — from scenario YAML fields
  B: source_fidelity — from tree-sitter context (optional)
  C: test_quality — always present, structural checks
  D: framework_compliance — from framework registry

Related: judge/rubric.py, judge/validator.py
"""

__all__: list[str] = []
