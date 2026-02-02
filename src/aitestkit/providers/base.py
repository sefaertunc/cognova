"""
Abstract LLM Provider Interface.

Defines the Protocol that all LLM providers must implement.
Uses Python's Protocol for structural subtyping (duck typing with type hints).

Classes:
    LLMProvider: Protocol for LLM providers

See MASTER_SPEC.md Section 5.1 for detailed specification.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """Abstract interface for LLM providers.

    All providers must implement these methods to be compatible with AITestKit.

    Properties:
        name: Provider identifier (e.g., 'claude', 'openai')

    Methods:
        generate: Text completion
        generate_with_attachments: Multimodal generation (images, PDFs)
    """

    @property
    def name(self) -> str:
        """Provider name (e.g., 'claude', 'openai')."""
        ...

    def generate(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> str:
        """Generate text completion."""
        ...

    def generate_with_attachments(
        self,
        prompt: str,
        model: str,
        attachments: list[dict],
        max_tokens: int = 4096,
    ) -> str:
        """Generate with multimodal input (images, PDFs, etc.)."""
        ...
