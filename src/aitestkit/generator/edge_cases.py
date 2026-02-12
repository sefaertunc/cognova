"""Edge-case test generation (v1.1 feature).

Separate MCP tool from main generation. Generates tests targeting:
    - Boundary values
    - Empty/null inputs
    - Maximum/minimum ranges
    - Type coercion edge cases
    - Concurrency edge cases (if applicable)

Uses higher temperature (0.7) for creative exploration.
Model: follows quality tier setting (standard=Sonnet, high=Opus).

Called by: mcp_server.py (generate_edge_cases tool)
"""


class EdgeCaseGenerator:
    """Generate edge-case focused tests.

    Methods:
        generate(scenario: Scenario, context: TargetContext, quality: str) -> GenerationResult
    """

    pass
