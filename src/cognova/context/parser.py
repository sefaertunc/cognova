"""tree-sitter parsing for supported languages.

Extracts from each source file:
    - Function/method signatures (name, params, types, return type)
    - Class definitions (name, bases, methods)
    - Import statements (what is imported, from where)
    - Module-level constants and type aliases

Does NOT extract:
    - Function bodies / implementation details
    - Comments (except docstrings for context)
    - Formatting or whitespace

Supported languages (priority order):
    1. Python (v1.0)
    2. TypeScript/JavaScript (v1.0)
    3. Java (v1.1)
    4. C# (v1.1)
    5. Scala (deferred)

Dependencies: tree-sitter, tree-sitter-python, tree-sitter-javascript, etc.
"""


class TreeSitterParser:
    """Parse source files into structural representations.

    Methods:
        parse_file(path: Path, language: str) -> FileStructure
        parse_directory(path: Path, languages: list[str]) -> list[FileStructure]
        get_supported_languages() -> list[str]
    """

    pass
