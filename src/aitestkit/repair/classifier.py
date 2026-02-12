"""Classify test failures into categories that determine repair strategy.

Categories:
    STRUCTURAL — ImportError, SyntaxError, TypeError, AttributeError, NameError
        → Repair loop: re-generate with error context (up to 3 attempts or $0.50)
        → Model: same as original generation (standard=Sonnet, high=Opus)

    ASSERTION — AssertionError, "DID NOT RAISE", expected vs actual mismatch
        → NOT repaired. Presented as FINDING to user.
        → repair_test tool refuses assertion failures with explanation.
        → Rationale: assertion failure may indicate the code-under-test has a bug,
          not that the test is wrong.

    UNKNOWN — Any other exception or unrecognized output
        → Present full output to user for manual decision.
        → User can choose to attempt repair or investigate manually.

Input: test execution output (stdout + stderr + exit code)
Output: FailureClassification with category, error type, relevant lines
"""


class FailureClassifier:
    """Classify test execution failures.

    Methods:
        classify(stdout: str, stderr: str, exit_code: int) -> FailureClassification
    """

    pass
