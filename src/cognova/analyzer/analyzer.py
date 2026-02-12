"""AI-powered failure analysis via Sonnet.

Receives raw test output (stdout + stderr + exit code).
Sends to Sonnet for root cause analysis.
Returns structured diagnosis — no separate report file.

In v3.2 this was split into analyzer/log_parser/report_generator.
In v4.0 it's a single module: parse + analyze + return structured result.
The MCP tool response IS the report — no file generation needed.

Called by: mcp_server.py (analyze_failure tool, Pipeline 8)
Model: Sonnet (analysis role)
"""


class FailureAnalyzer:
    """Analyze test failure logs and provide root cause diagnosis.

    Methods:
        analyze(log_content: str) -> AnalysisResult

    AnalysisResult contains:
        - root_cause: str
        - suggestion: str
        - affected_files: list[str]
        - severity: str ("low" | "medium" | "high" | "critical")
        - category: str ("structural" | "assertion" | "environment" | "unknown")
    """

    pass
