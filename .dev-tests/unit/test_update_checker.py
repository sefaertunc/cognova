import json
from unittest.mock import MagicMock, patch

from cognova.utils.update_checker import UpdateChecker, UpdateInfo


def test_update_info_creation():
    info = UpdateInfo(current="1.0.0", latest="1.1.0", update_available=True)
    assert info.current == "1.0.0"
    assert info.latest == "1.1.0"
    assert info.update_available is True


def test_update_info_no_update():
    info = UpdateInfo(current="1.0.0", latest="1.0.0", update_available=False)
    assert info.update_available is False


def _mock_pypi_response(version: str) -> MagicMock:
    """Create a mock urlopen response returning a given version."""
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"info": {"version": version}}).encode()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


@patch("cognova.utils.update_checker.urllib.request.urlopen")
def test_check_returns_update_info_when_outdated(mock_urlopen):
    mock_urlopen.return_value = _mock_pypi_response("2.0.0")
    checker = UpdateChecker(current_version="1.0.0")
    result = checker.check()
    assert isinstance(result, UpdateInfo)
    assert result.current == "1.0.0"
    assert result.latest == "2.0.0"
    assert result.update_available is True


@patch("cognova.utils.update_checker.urllib.request.urlopen")
def test_check_returns_none_when_current(mock_urlopen):
    mock_urlopen.return_value = _mock_pypi_response("1.0.0")
    checker = UpdateChecker(current_version="1.0.0")
    assert checker.check() is None


@patch("cognova.utils.update_checker.urllib.request.urlopen")
def test_check_returns_none_on_network_error(mock_urlopen):
    mock_urlopen.side_effect = ConnectionError("no internet")
    checker = UpdateChecker(current_version="1.0.0")
    assert checker.check() is None


@patch("cognova.utils.update_checker.urllib.request.urlopen")
def test_check_returns_none_on_timeout(mock_urlopen):
    mock_urlopen.side_effect = TimeoutError("timed out")
    checker = UpdateChecker(current_version="1.0.0")
    assert checker.check() is None


@patch("cognova.utils.update_checker.urllib.request.urlopen")
def test_check_uses_correct_pypi_url(mock_urlopen):
    mock_urlopen.return_value = _mock_pypi_response("1.0.0")
    checker = UpdateChecker(current_version="1.0.0")
    checker.check()
    call_args = mock_urlopen.call_args
    req = call_args[0][0]
    assert req.full_url == "https://pypi.org/pypi/cognova-mcp/json"


def test_update_checker_importable():
    import cognova.utils.update_checker as mod
    assert mod.UpdateChecker is not None
    assert mod.UpdateInfo is not None
