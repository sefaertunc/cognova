"""Claude/Anthropic Provider Implementation.

Implements the LLMProvider protocol for Anthropic's Claude models.
This is the primary (and only) provider in v1.0.

Resolves model by role + quality tier from ProjectConfig.
Returns actual model string used (for cost logging via cost_tracker).
Supports extended thinking for Opus 4.6 (adaptive thinking parameter).

Classes:
    ClaudeProvider: Claude implementation of LLMProvider
"""

from typing import Any, cast

import anthropic
from pydantic_core import ValidationError

from cognova.config import SONNET_MODEL, ProjectConfig, get_settings
from cognova.errors import APIAuthError, APIRateLimitError, APITimeoutError
from cognova.providers.base import LLMResponse, TokenUsage


class ClaudeProvider:
    """Claude/Anthropic implementation of LLMProvider.

    Resolves model selection from role + quality tier.
    Returns LLMResponse with model string and token usage for cost tracking.
    """

    name = "claude"

    def __init__(self) -> None:
        """Initialize Claude provider. Requires ANTHROPIC_API_KEY."""
        try:
            self._settings = get_settings()
        except ValidationError:
            raise APIAuthError("The API key not found.") from None
        self._config = ProjectConfig()
        self._client = anthropic.Anthropic(api_key=self._settings.anthropic_api_key)

    def complete(
        self,
        prompt: str,
        role: str,
        quality: str = "standard",
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> LLMResponse:
        """Generate text completion using Claude.

        Resolves model from role + quality tier via config.
        Returns LLMResponse with actual model string and token usage.
        """
        model = self._config.get_model_for_role(role=role, quality=quality)
        try:
            response = self._client.messages.create(model=model, max_tokens=max_tokens, temperature=temperature, messages=[{"role": "user", "content": prompt}], stream=False)
        except anthropic.AuthenticationError:
            raise APIAuthError("API key not authenticated.") from None
        except anthropic.RateLimitError:
            raise APIRateLimitError("Rate limit exceeded.") from None
        except anthropic.APITimeoutError:
            raise APITimeoutError("Request timed out.") from None
        text_block = cast(anthropic.types.TextBlock, response.content[0])
        usage = TokenUsage(input_tokens=response.usage.input_tokens, output_tokens=response.usage.output_tokens)
        return LLMResponse(content=text_block.text, model=response.model, usage=usage)

    def complete_with_attachments(
        self,
        prompt: str,
        role: str,
        attachments: list[dict[str, Any]],
        quality: str = "standard",
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """Generate with multimodal input using Claude's vision capabilities."""
        model = self._config.get_model_for_role(role=role, quality=quality)
        content_blocks: list[Any] = [*attachments, {"type": "text", "text": prompt}]
        try:
            response = self._client.messages.create(model=model, max_tokens=max_tokens, messages=[{"role": "user", "content": content_blocks}], stream=False)
        except anthropic.AuthenticationError:
            raise APIAuthError("API key not authenticated.") from None
        except anthropic.RateLimitError:
            raise APIRateLimitError("Rate limit exceeded.") from None
        except anthropic.APITimeoutError:
            raise APITimeoutError("Request timed out.") from None
        text_block = cast(anthropic.types.TextBlock, response.content[0])
        usage = TokenUsage(input_tokens=response.usage.input_tokens, output_tokens=response.usage.output_tokens)
        return LLMResponse(content=text_block.text, model=response.model, usage=usage)

    def count_tokens(self, text: str) -> int:
        """Count tokens using Anthropic's token counting API."""
        result = self._client.messages.count_tokens(model=SONNET_MODEL, messages=[{"role": "user", "content": text}])
        return result.input_tokens
