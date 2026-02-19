"""Shared pytest configuration and fixtures for dev_tests."""

import os
import pytest
from pathlib import Path
from cognova.providers.base import (
    TokenUsage,
    LLMResponse,
)

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class MockProvider:
    """Minimal class that satisfies LLMProvider protocol."""

    @property
    def name(self) -> str:
        return "mock"

    def complete(self, prompt, role, quality="standard", max_tokens=4096, temperature=0.0):
        return LLMResponse(
            content="mock response",
            model="mock-model",
            usage=TokenUsage(input_tokens=10, output_tokens=5),
        )

    def complete_with_attachments(
        self, prompt, role, attachments, quality="standard", max_tokens=4096
    ):
        return LLMResponse(
            content="mock response",
            model="mock-model",
            usage=TokenUsage(input_tokens=10, output_tokens=5),
        )

    def count_tokens(self, text):
        return len(text.split())


@pytest.fixture
def mock_provider_class():
    """Return MockProvider class for registry tests."""
    return MockProvider


@pytest.fixture(autouse=True)
def clean_registry():
    """Reset provider registry between tests."""
    from cognova.providers import registry
    original_providers = dict(registry._PROVIDERS)
    original_tiers = dict(registry._PROVIDER_TIERS)
    registry._PROVIDERS.clear()
    registry._PROVIDER_TIERS.clear()
    registry._PROVIDER_TIERS["claude"] = 1
    yield
    registry._PROVIDERS.clear()
    registry._PROVIDERS.update(original_providers)
    registry._PROVIDER_TIERS.clear()
    registry._PROVIDER_TIERS.update(original_tiers)

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
COGNOVA_QUALITY_TIER=standard
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

@pytest.fixture
def mock_settings(monkeypatch):
    """Provide Settings with fake API key, clearing lru_cache."""
    from cognova.config import get_settings
    get_settings.cache_clear()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-12345")
    settings = get_settings()
    yield settings
    get_settings.cache_clear()


@pytest.fixture
def mock_config():
    """Provide default ProjectConfig for tests."""
    from cognova.config import ProjectConfig
    return ProjectConfig()


@pytest.fixture
def mock_anthropic_client(mocker):
    """Patch anthropic.Anthropic and return a mock client with realistic response."""
    from unittest.mock import MagicMock

    mock_usage = MagicMock()
    mock_usage.input_tokens = 100
    mock_usage.output_tokens = 50

    mock_text_block = MagicMock()
    mock_text_block.text = "mock response"
    mock_text_block.type = "text"

    mock_response = MagicMock()
    mock_response.content = [mock_text_block]
    mock_response.model = "claude-sonnet-4-5-20250514"
    mock_response.usage = mock_usage

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_response

    mock_count_result = MagicMock()
    mock_count_result.input_tokens = 42
    mock_client.messages.count_tokens.return_value = mock_count_result

    mocker.patch("anthropic.Anthropic", return_value=mock_client)

    return mock_client


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "requires_api: mark test as requiring real API key"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
