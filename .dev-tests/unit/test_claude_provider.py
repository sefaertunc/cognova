import pytest
from cognova.providers.claude import ClaudeProvider
from cognova.providers.base import LLMProvider
from cognova.errors import APIAuthError


def test_claude_provider_creation(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    assert isinstance(provider, ClaudeProvider)


def test_claude_provider_name(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    assert provider.name == "claude"


def test_claude_provider_is_llm_provider(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    assert isinstance(provider, LLMProvider)


def test_claude_provider_missing_api_key():
    with pytest.raises(APIAuthError):
        ClaudeProvider()
