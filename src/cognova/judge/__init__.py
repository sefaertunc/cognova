"""
Rubric-based LLM-as-Judge module.

Uses Claude Haiku to evaluate generated test code against a dynamic
binary checklist. Each criterion is a concrete yes/no question derived
from scenario YAML, tree-sitter source context, and framework registry.

Components:
- criteria.py: Criterion dataclass, Category enum, framework criteria registry
- rubric.py: RubricBuilder — dynamic criteria from inputs
- validator.py: JudgeValidator — orchestrates build → Haiku → parse → verdict

Exports:
- JudgeValidator: Orchestrator class
- JudgeResult: Complete evaluation result
- RubricBuilder: Builds criteria list from inputs
- Criterion, CriterionResult: Data classes
- Category: Criterion category enum

See MASTER_SPEC.md Section 4.6 (F022) for full specification.
"""

__all__: list[str] = []
