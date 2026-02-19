"""LLM-as-Judge orchestrator.

Builds rubric → formats prompt → calls Haiku → parses response → computes verdict.

Pipeline: build_rubric() → format_prompt() → Haiku API call → parse_response() → compute_verdict()

Classes:
- JudgeResult: Complete evaluation result (verdict, score, criteria, failed_criteria, hard_fails)
- JudgeValidator: Orchestrator — async evaluate() runs the full pipeline

Verdict logic:
  PASS: score >= threshold AND zero hard-fail criteria failed
  WARN: score >= (threshold - buffer) AND zero hard-fail criteria failed
  FAIL: score < (threshold - buffer) OR any hard-fail criterion failed

Config: judge.pass_threshold (default 70), judge.warn_buffer (default 15)

Related: judge/rubric.py, judge/criteria.py, prompts/templates/judge/evaluate.md
"""

__all__: list[str] = []
