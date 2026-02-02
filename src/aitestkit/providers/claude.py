"""
Claude/Anthropic Provider Implementation.

Implements the LLMProvider protocol for Anthropic's Claude models.
This is the primary (and only) provider in v1.0.

Classes:
    ClaudeProvider: Claude implementation of LLMProvider

Migration Note:
    This module replaces utils/claude_client.py. Migrate existing logic here.

See MASTER_SPEC.md Section 5.2 for detailed specification.
"""

# TODO: Migrate from utils/claude_client.py


class ClaudeProvider:
    """Claude/Anthropic implementation of LLMProvider."""

    name = "claude"

    def __init__(self) -> None:
        """Initialize Claude provider. Requires ANTHROPIC_API_KEY."""
        # TODO: Initialize Anthropic client
        pass

    def generate(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> str:
        """Generate text completion using Claude."""
        # TODO: Implement - migrate from utils/claude_client.py
        raise NotImplementedError("ClaudeProvider.generate not implemented")

    def generate_with_attachments(
        self,
        prompt: str,
        model: str,
        attachments: list[dict],
        max_tokens: int = 4096,
    ) -> str:
        """Generate with multimodal input using Claude's vision capabilities."""
        # TODO: Implement vision/document support
        raise NotImplementedError("ClaudeProvider.generate_with_attachments not implemented")
