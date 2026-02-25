"""
Scenario YAML loader.

Loads and parses scenario YAML files into Pydantic models.

Classes:
Functions:
- load_scenario(path) -> ScenarioFile: Load and validate scenario file
- load_scenario_raw(path) -> dict: Load scenario as raw dictionary
- detect_language(file_path) -> str: Detect programming language from file extension
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from cognova.errors import ScenarioLoadError, ScenarioValidationError
from cognova.scenario.validator import ScenarioFile

# Code file extension to language mapping.
# Used for:
# 1. Auto-detecting programming language from file extension
# 2. Proper code block formatting with language hint (```python, ```csharp, etc.)
# 3. Validation warnings for unknown extensions
CODE_EXTENSIONS: dict[str, str] = {
    # Python
    ".py": "python",
    ".pyw": "python",
    ".pyi": "python",

    # JavaScript/TypeScript
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".jsx": "jsx",
    ".ts": "typescript",
    ".tsx": "typescript",

    # JVM Languages
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".scala": "scala",
    ".groovy": "groovy",
    ".clj": "clojure",

    # .NET Languages
    ".cs": "csharp",
    ".vb": "vb",
    ".fs": "fsharp",
    ".fsx": "fsharp",

    # Systems Languages
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".hxx": "cpp",
    ".go": "go",
    ".rs": "rust",

    # Scripting Languages
    ".rb": "ruby",
    ".php": "php",
    ".pl": "perl",
    ".pm": "perl",
    ".lua": "lua",
    ".r": "r",
    ".R": "r",

    # Shell
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "zsh",
    ".ps1": "powershell",
    ".psm1": "powershell",
    ".bat": "batch",
    ".cmd": "batch",

    # Mobile
    ".swift": "swift",
    ".m": "objectivec",
    ".mm": "objectivec",
    ".dart": "dart",

    # Web Frameworks
    ".vue": "vue",
    ".svelte": "svelte",

    # Functional Languages
    ".hs": "haskell",
    ".ex": "elixir",
    ".exs": "elixir",
    ".erl": "erlang",
    ".ml": "ocaml",
    ".elm": "elm",

    # Data/Config
    ".sql": "sql",
    ".graphql": "graphql",
    ".gql": "graphql",

    # Other
    ".zig": "zig",
    ".nim": "nim",
    ".v": "v",
    ".cr": "crystal",
}


def detect_language(file_path: str | Path) -> str:
    """Detect programming language from file extension.

    Args:
        file_path: Path to the code file

    Returns:
        Language identifier for code block hint (e.g., 'python', 'csharp'),
        or 'text' for unknown extensions
    """
    ext = Path(file_path).suffix.lower()
    return CODE_EXTENSIONS.get(ext, "text")

def load_scenario_raw(path: Path) -> dict[str, Any]:
    """Load scenario YAML as raw dictionary."""
    if not path.exists():
        raise ScenarioLoadError(path, "File not found")
    try:
        with open(path) as d:
            data = yaml.safe_load(d)
    except yaml.YAMLError as e:
        raise ScenarioLoadError(path, f"Invalid YAML: {e}") from e
    if not isinstance(data, dict):
        raise ScenarioLoadError(path, "Scenario must be a YAML mapping, not a scalar or list")
    return data


def load_scenario(path: Path) -> ScenarioFile:
    """Load and validate scenario YAML into Pydantic model."""
    data = load_scenario_raw(path)
    try:
        return ScenarioFile(**data)
    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        raise ScenarioValidationError(path, errors) from e
