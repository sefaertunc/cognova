"""Abstract LLM Provider Interface.

Defines the Protocol that all LLM providers must implement.
Uses Python's Protocol for structural subtyping (duck typing with type hints).

Classes:
    LLMProvider: Protocol for LLM providers
    LLMResponse: Structured response including model and usage info
    TokenUsage: Token count details
"""

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass
class TokenUsage:
    """Token usage from an API call."""

    input_tokens: int
    output_tokens: int


@dataclass
class LLMResponse:
    """Structured LLM response with metadata for cost tracking."""

    content: str
    model: str
    usage: TokenUsage


@runtime_checkable
class LLMProvider(Protocol):
    """Abstract interface for LLM providers.

    All providers must implement these methods to be compatible with Cognova.
    The complete() method returns LLMResponse with model string and token usage
    so that cost_tracker can log the actual model used.
    """

    @property
    def name(self) -> str:
        """Provider name (e.g., 'claude', 'openai')."""
        ...

    def complete(
        self,
        prompt: str,
        role: str,
        quality: str = "standard",
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> LLMResponse:
        """Generate text completion.

        Args:
            prompt: The prompt to send
            role: Model role ("generation", "analysis", "validation")
            quality: Quality tier ("standard" or "high")
            max_tokens: Maximum output tokens
            temperature: Sampling temperature

        Returns:
            LLMResponse with content, model string, and token usage
        """
        ...

    def complete_with_attachments(
        self,
        prompt: str,
        role: str,
        attachments: list[dict[str, Any]],
        quality: str = "standard",
        max_tokens: int = 4096,
    ) -> LLMResponse:
        """Generate with multimodal input (images, PDFs, etc.)."""
        ...

    def count_tokens(self, text: str) -> int:
        """Count tokens in the given text."""
        ...
