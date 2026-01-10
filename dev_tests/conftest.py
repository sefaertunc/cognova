"""Shared pytest configuration and fixtures for dev_tests."""

import os
import pytest
from pathlib import Path

# Add src to Python path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def project_root():
    """Get project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_env_file(tmp_path):
    """Create temporary .env file for testing."""
    env_file = tmp_path / ".env"
    env_file.write_text("""
ANTHROPIC_API_KEY=test-key-12345
AITESTKIT_MODEL_CODE_GEN=claude-opus-4-5-20251101
AITESTKIT_MODEL_ANALYSIS=claude-sonnet-4-5-20250929
AITESTKIT_MODEL_REGRESSION=claude-haiku-4-5-20251001
""".strip())
    return env_file


@pytest.fixture
def mock_api_key(monkeypatch):
    """Set mock API key in environment."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-12345")


@pytest.fixture
def has_real_api_key():
    """Check if real API key is available."""
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "requires_api: mark test as requiring real API key"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
