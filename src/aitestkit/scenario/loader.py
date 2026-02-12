"""
Scenario YAML loader.

Loads and parses scenario YAML files into Pydantic models.

Classes:
- Target: Target system/feature being tested
- Scenarios: Test scenarios grouped by outcome type
- ScenarioFile: Complete scenario YAML file structure

Functions:
- load_scenario(path) -> ScenarioFile: Load and validate scenario file
- load_scenario_raw(path) -> dict: Load scenario as raw dictionary
- detect_language(file_path) -> str: Detect programming language from file extension

See MASTER_SPEC.md Section 9.4 for schema details.

TODO: Implement loader classes and functions
"""

from pathlib import Path

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


# New v4.0 fields for scenario YAML
SCENARIO_V4_FIELDS = {
    "quality": "standard",       # "standard" (Sonnet) or "high" (Opus)
    "edge_cases": False,         # Generate edge-case focused tests separately
    "fault_analysis": False,     # Generate fault-guided tests (ACH pattern)
}


# Placeholder - loader implementation to follow
