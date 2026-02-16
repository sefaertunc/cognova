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


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "requires_api: mark test as requiring real API key"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
