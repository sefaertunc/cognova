from pathlib import Path

import pytest

import cognova.errors
from cognova.errors import (
    APIAuthError,
    APIError,
    APIRateLimitError,
    APITimeoutError,
    CognovaError,
    EmptyResponseError,
    GenerationError,
    LanceDBError,
    ScenarioValidationError,
    StorageError,
    UserInputError,
    __all__,
)


@pytest.mark.parametrize(
    "error_cls, parents",
    [
        (UserInputError, (CognovaError, Exception)),
        (ScenarioValidationError, (UserInputError, CognovaError)),
        (APIAuthError, (APIError, CognovaError)),
        (APIRateLimitError, (APIError, CognovaError)),
        (APITimeoutError, (APIError, CognovaError)),
        (EmptyResponseError, (GenerationError, CognovaError)),
        (LanceDBError, (StorageError, CognovaError)),
    ],
)
def test_hierarchy(error_cls, parents):
    if error_cls is ScenarioValidationError:
        exc = error_cls(Path("test.yaml"), ["err"])
    else:
        exc = error_cls()
    for parent in parents:
        assert isinstance(exc, parent)


@pytest.mark.parametrize(
    "error_cls, expected_code",
    [
        (CognovaError, 1),
        (UserInputError, 2),
        (ScenarioValidationError, 2),
        (APIError, 3),
        (APIAuthError, 3),
        (APIRateLimitError, 3),
        (APITimeoutError, 3),
        (GenerationError, 4),
        (EmptyResponseError, 4),
        (StorageError, 5),
        (LanceDBError, 5),
    ],
)
def test_exit_codes(error_cls, expected_code):
    assert error_cls.exit_code == expected_code


@pytest.mark.parametrize(
    "error_cls, message",
    [
        (CognovaError, "test"),
        (CognovaError, ""),
        (APIAuthError, "bad key"),
        (UserInputError, "invalid input"),
    ],
)
def test_message(error_cls, message):
    exc = error_cls(message)
    assert str(exc) == message
    assert exc.message == message


def test_default_message_is_empty():
    exc = CognovaError()
    assert str(exc) == ""
    assert exc.message == ""


def test_scenario_validation_error_carries_data():
    exc = ScenarioValidationError(Path("login.yaml"), ["missing target", "no failures"])
    assert exc.file == Path("login.yaml")
    assert exc.errors == ["missing target", "no failures"]
    assert "login.yaml" in str(exc)
    assert "2 errors" in str(exc)


def test_scenario_validation_error_single_error():
    exc = ScenarioValidationError(Path("x.yaml"), ["one problem"])
    assert len(exc.errors) == 1
    assert "1 errors" in str(exc)


def test_rate_limit_with_retry_after():
    exc = APIRateLimitError(retry_after=45)
    assert exc.retry_after == 45
    assert "45" in str(exc)
    assert "retry after" in str(exc).lower()


def test_rate_limit_without_retry_after():
    exc = APIRateLimitError("custom msg")
    assert exc.retry_after == 0
    assert str(exc) == "custom msg"


def test_rate_limit_default():
    exc = APIRateLimitError()
    assert exc.retry_after == 0
    assert str(exc) == "Rate limit exceeded"


@pytest.mark.parametrize(
    "raise_cls, catch_cls",
    [
        (APIAuthError, APIError),
        (APIRateLimitError, APIError),
        (APITimeoutError, APIError),
        (LanceDBError, StorageError),
        (EmptyResponseError, GenerationError),
        (ScenarioValidationError, UserInputError),
        (UserInputError, CognovaError),
        (StorageError, CognovaError),
    ],
)
def test_catchability(raise_cls, catch_cls):
    if raise_cls is ScenarioValidationError:
        exc = raise_cls(Path("t.yaml"), ["err"])
    else:
        exc = raise_cls("test")
    with pytest.raises(catch_cls):
        raise exc


def test_all_exports_count():
    assert len(__all__) == 12


def test_no_builtin_memory_error_shadow():
    assert not hasattr(cognova.errors, "MemoryError")
    assert "MemoryError" not in __all__
