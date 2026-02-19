"""Dynamic rubric builder.

Constructs criteria list from scenario YAML, source code context,
and framework. Structure is fixed (4 categories); content is populated
from inputs.

Class:
- RubricBuilder: build(scenario, source_context, framework) → list[Criterion]

Category population:
  A (Scenario Alignment): Always present. From scenario target, description, steps, edge_cases.
  B (Source Code Fidelity): Only when tree-sitter context available. Fixed set of 4 criteria.
  C (Test Quality): Always present. Fixed set of 5 criteria. Contains hard-fail items.
  D (Framework Compliance): From get_framework_criteria(). Falls back to generic.

Safety cap: max_criteria (default 20) truncates rubric if too many criteria generated.

Related: judge/criteria.py, judge/validator.py
"""

__all__: list[str] = []
