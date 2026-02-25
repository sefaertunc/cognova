from __future__ import annotations

from pathlib import Path

__all__ = [
    "CognovaError",
    "UserInputError",
    "ScenarioValidationError",
    "APIError",
    "APIAuthError",
    "APIRateLimitError",
    "APITimeoutError",
    "GenerationError",
    "EmptyResponseError",
    "StorageError",
    "LanceDBError",
    "ProviderNotFoundError",
    "ScenarioLoadError"
]


class CognovaError(Exception):
    """Base exception for all Cognova errors."""

    exit_code: int = 1

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(message)


class UserInputError(CognovaError):
    """User provided invalid input."""

    exit_code = 2


class ScenarioValidationError(UserInputError):
    """Scenario YAML failed validation."""

    def __init__(self, file: Path, errors: list[str]) -> None:
        self.file = file
        self.errors = errors
        super().__init__(f"Scenario validation failed: {file} ({len(errors)} errors)")


class ScenarioLoadError(UserInputError):
    """Scenario YAML file does not exist in defined path"""
    def __init__(self, file: Path, reason: str) -> None:
        self.file = file
        self.reason = reason
        super().__init__(f"Cannot load scenario: {file} ({reason})")


class APIError(CognovaError):
    """Claude API call failed."""

    exit_code = 3


class APIAuthError(APIError):
    """Invalid or missing API key."""


class APIRateLimitError(APIError):
    """Rate limit exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", *, retry_after: int = 0) -> None:
        self.retry_after = retry_after
        if retry_after:
            message = f"{message} (retry after {retry_after}s)"
        super().__init__(message)


class APITimeoutError(APIError):
    """Request timed out."""


class GenerationError(CognovaError):
    """Code generation failed."""

    exit_code = 4


class EmptyResponseError(GenerationError):
    """AI returned empty or unparseable response."""


class StorageError(CognovaError):
    """Storage operation failed."""

    exit_code = 5


class LanceDBError(StorageError):
    """LanceDB database error."""


class ProviderNotFoundError(CognovaError):
    """Missing or unknown provider error."""

    exit_code = 6
