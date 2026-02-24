"""Check for Cognova updates on startup.

For users who pin a version (not using @latest):
    On MCP server startup, compare __version__ to latest on PyPI.
    If outdated, include update notice in first tool response.

Does NOT auto-update. Only notifies.
Network call: single GET to PyPI JSON API.
Timeout: 2 seconds. Failure is silent (no error to user).
"""

import json
import urllib.request
from dataclasses import dataclass

from packaging.version import Version

PYPI_URL = "https://pypi.org/pypi/{package}/json"
TIMEOUT_SECONDS = 2


@dataclass
class UpdateInfo:
    """Result of an update check."""

    current: str
    latest: str
    update_available: bool


class UpdateChecker:
    """Check PyPI for newer Cognova versions."""

    def __init__(self, current_version: str, package_name: str = "cognova-mcp") -> None:
        self.current_version = current_version
        self.package_name = package_name

    def check(self) -> UpdateInfo | None:
        """Compare local version to PyPI latest. Returns None if current or on any error."""
        try:
            url = PYPI_URL.format(package=self.package_name)
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                data = json.loads(resp.read())
            latest = data["info"]["version"]

            if Version(latest) > Version(self.current_version):
                return UpdateInfo(
                    current=self.current_version,
                    latest=latest,
                    update_available=True,
                )
            return None
        except Exception:
            return None
