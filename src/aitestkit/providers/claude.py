"""Claude/Anthropic Provider Implementation.

Implements the LLMProvider protocol for Anthropic's Claude models.
This is the primary (and only) provider in v1.0.

Resolves model by role + quality tier from ProjectConfig.
Returns actual model string used (for cost logging via cost_tracker).
Supports extended thinking for Opus 4.6 (adaptive thinking parameter).

Classes:
    ClaudeProvider: Claude implementation of LLMProvider
"""

from aitestkit.providers.base import LLMResponse


class ClaudeProvider:
    """Claude/Anthropic implementation of LLMProvider.

    Resolves model selection from role + quality tier.
    Returns LLMResponse with model string and token usage for cost tracking.
    """

    name = "claude"

    def __init__(self) -> None:
        """Initialize Claude provider. Requires ANTHROPIC_API_KEY."""
        raise NotImplementedError("ClaudeProvider.__init__ not implemented")

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
        raise NotImplementedError("ClaudeProvider.complete not implemented")

    def complete_with_attachments(
        self,
        prompt: str,
        role: str,
        attachments: list[dict],
        quality: str = "standard",
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """Generate with multimodal input using Claude's vision capabilities."""
        raise NotImplementedError("ClaudeProvider.complete_with_attachments not implemented")

    def count_tokens(self, text: str) -> int:
        """Count tokens using Anthropic's token counting API."""
        raise NotImplementedError("ClaudeProvider.count_tokens not implemented")
