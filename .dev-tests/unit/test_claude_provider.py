import pytest
from cognova.providers.claude import ClaudeProvider
from cognova.providers.base import LLMProvider, LLMResponse
from cognova.errors import APIAuthError, APIRateLimitError, APITimeoutError
from pydantic_core import ValidationError
from cognova.config import HAIKU_MODEL, OPUS_MODEL
import anthropic


def test_claude_provider_creation(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    assert isinstance(provider, ClaudeProvider)


def test_claude_provider_name(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    assert provider.name == "claude"


def test_claude_provider_is_llm_provider(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    assert isinstance(provider, LLMProvider)


def test_claude_provider_missing_api_key(mocker):
    mocker.patch(
        "cognova.providers.claude.get_settings",
        side_effect=ValidationError.from_exception_data(
            title="Settings",
            line_errors=[],
        ),
    )
    with pytest.raises(APIAuthError):
        ClaudeProvider()


def test_complete_returns_llm_response(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    response = provider.complete("sample prompt", "generation")
    assert isinstance(response, LLMResponse)
    assert response.content == "mock response"
    assert response.model == "claude-sonnet-4-5-20250514"
    assert response.usage.input_tokens == 100
    assert response.usage.output_tokens == 50


def test_complete_resolves_model_from_role(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    provider.complete("sample prompt", "validation")
    call_kwargs = mock_anthropic_client.messages.create.call_args.kwargs
    assert call_kwargs["model"] == HAIKU_MODEL


def test_complete_high_quality_uses_opus(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    provider.complete("sample prompt", "generation", quality="high")
    call_kwargs = mock_anthropic_client.messages.create.call_args.kwargs
    assert call_kwargs["model"] == OPUS_MODEL


@pytest.mark.parametrize(
    "anthropic_error, cognova_error",
    [
        (anthropic.AuthenticationError, APIAuthError),
        (anthropic.RateLimitError, APIRateLimitError),
    ],
)
def test_complete_api_errors(mock_settings, mock_anthropic_client, anthropic_error, cognova_error):
    from unittest.mock import MagicMock

    provider = ClaudeProvider()
    mock_response = MagicMock()
    mock_response.request = MagicMock()
    mock_anthropic_client.messages.create.side_effect = anthropic_error(
        message="api error",
        response=mock_response,
        body=None,
    )
    with pytest.raises(cognova_error):
        provider.complete("sample prompt", "generation")


def test_complete_timeout_error(mock_settings, mock_anthropic_client):
    from unittest.mock import MagicMock

    provider = ClaudeProvider()
    mock_anthropic_client.messages.create.side_effect = anthropic.APITimeoutError(
        request=MagicMock(),
    )
    with pytest.raises(APITimeoutError):
        provider.complete("sample prompt", "generation")


def test_count_tokens(mock_settings, mock_anthropic_client):
    provider = ClaudeProvider()
    token_amount = provider.count_tokens("sample sentence")
    assert token_amount == 42


def test_complete_with_attachments(mock_settings, mock_anthropic_client):
    attachment = {
        "type": "image",
        "source": {"type": "base64", "media_type": "image/png", "data": "abc123"},
    }
    provider = ClaudeProvider()
    response = provider.complete_with_attachments(
        "describe this image",
        "generation",
        [attachment],
    )
    assert isinstance(response, LLMResponse)
    assert response.content == "mock response"
    call_kwargs = mock_anthropic_client.messages.create.call_args.kwargs
    content_blocks = call_kwargs["messages"][0]["content"]
    assert content_blocks[0] == attachment
    assert content_blocks[-1] == {"type": "text", "text": "describe this image"}
