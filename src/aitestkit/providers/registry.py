"""
Provider Registry.

Central registry for LLM providers with tier-based categorization.

Tiers:
    1 - Recommended: Fully tested, optimized prompts (Claude)
    2 - Compatible: Basic testing done, should work (Future: OpenAI, Gemini)
    3 - Experimental: Use at own risk, no guarantees (Future: Ollama, local models)

See MASTER_SPEC.md Section 5.3 for detailed specification.
"""

from typing import Type

_PROVIDERS: dict[str, Type] = {}

_PROVIDER_TIERS: dict[str, int] = {
    "claude": 1,  # Tier 1: Recommended
}


def get_provider(name: str = "claude"):
    """Get provider instance by name."""
    if name not in _PROVIDERS:
        available = list(_PROVIDERS.keys())
        raise ValueError(f"Unknown provider: {name}. Available: {available}")
    return _PROVIDERS[name]()


def register_provider(name: str, provider_class: Type, tier: int = 3) -> None:
    """Register a new provider."""
    _PROVIDERS[name] = provider_class
    _PROVIDER_TIERS[name] = tier


def get_provider_tier(name: str) -> int:
    """Get provider support tier (1=recommended, 2=compatible, 3=experimental)."""
    return _PROVIDER_TIERS.get(name, 3)


def list_providers() -> list[str]:
    """List all registered provider names."""
    return list(_PROVIDERS.keys())
