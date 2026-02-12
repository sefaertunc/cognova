"""Check for AITestKit updates on startup.

For users who pin a version (not using @latest):
    On MCP server startup, compare __version__ to latest on PyPI.
    If outdated, include update notice in first tool response.

Does NOT auto-update. Only notifies.
Network call: single GET to PyPI JSON API.
Timeout: 2 seconds. Failure is silent (no error to user).
"""


class UpdateChecker:
    """Check PyPI for newer AITestKit versions.

    Methods:
        check() -> UpdateInfo | None
    """

    pass
