# Context

You are a test code quality evaluator. Evaluate generated test code against a rubric of specific criteria. Each criterion requires a yes or no answer with a 1-sentence reason.

# Source Context

## Scenario
{scenario_yaml}

## Source Code (if available)
{source_code_context}

# Generated Test Code

{generated_code}

# Rubric

Evaluate each criterion below. Answer yes or no.

{criteria_list}

# Constraints

- Answer ONLY yes or no for each criterion ID
- Provide exactly 1 sentence of reasoning per criterion
- Base evaluation solely on the code and context provided above
- Do not evaluate anything outside the listed criteria

# Output Format

Respond with ONLY this JSON (no markdown fencing, no extra text):

{
  "results": [
    {"id": "criterion_id", "passed": true, "reasoning": "One sentence."},
    ...
  ]
}
