"""
LLM Provider Abstraction Layer.

This module provides a unified interface for interacting with different LLM providers.
In v1.0, only Claude is supported. Future versions may add OpenAI, Gemini, etc.

Exports:
    LLMProvider: Protocol defining the provider interface
    ClaudeProvider: Claude/Anthropic implementation
    get_provider: Factory function to get provider by name
    register_provider: Register custom providers
    get_provider_tier: Get provider support tier (1=recommended, 2=compatible, 3=experimental)

Example:
    >>> from cognova.providers import get_provider
    >>> provider = get_provider("claude")
    >>> response = provider.generate(prompt="...", model="claude-opus-4-5-20250514")

See MASTER_SPEC.md Section 5 for detailed specification.
"""

# TODO: Implement exports after base.py, claude.py, registry.py are complete
