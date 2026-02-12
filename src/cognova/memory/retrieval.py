"""CEDAR retrieval — Context-aware Example Dynamic Adaptive Retrieval.

Given a new test scenario, find the most relevant approved tests as few-shot examples.

CEDAR scoring:
    score = (w_code * code_similarity) + (w_text * text_similarity)
    Default weights: w_code = 0.6, w_text = 0.4

Process:
    1. Embed scenario text (MiniLM) and target code (UniXcoder)
    2. Search LanceDB for top-K by each embedding type
    3. Combine scores using CEDAR weighting
    4. Filter: exclude healed (not re-approved) tests
    5. Return top 1-2 examples for few-shot injection

Negative examples (rejected tests) are NOT used for few-shot.
Rejection data → MAPS rule analysis instead.
"""


class CEDARRetriever:
    """Retrieve few-shot examples via CEDAR scoring.

    Methods:
        retrieve(
            scenario_text: str,
            target_code: str,
            framework: str,
            top_k: int = 2
        ) -> list[FewShotExample]
    """

    pass
