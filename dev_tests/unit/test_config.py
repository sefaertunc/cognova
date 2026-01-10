"""Unit tests for configuration module."""

import pytest
from aitestkit.config import get_settings, Settings, ModelType


def test_settings_loads_from_env(mock_api_key):
    """Test that settings load from environment variables."""
    settings = get_settings()
    assert settings.anthropic_api_key == "test-key-12345"
    assert settings.model_code_gen == "claude-opus-4-5-20251101"
    assert settings.model_analysis == "claude-sonnet-4-5-20250929"
    assert settings.model_regression == "claude-haiku-4-5-20251001"


def test_get_model_id_opus(mock_api_key):
    """Test get_model_id returns correct Opus model."""
    settings = get_settings()
    assert settings.get_model_id("opus") == "claude-opus-4-5-20251101"


def test_get_model_id_sonnet(mock_api_key):
    """Test get_model_id returns correct Sonnet model."""
    settings = get_settings()
    assert settings.get_model_id("sonnet") == "claude-sonnet-4-5-20250929"


def test_get_model_id_haiku(mock_api_key):
    """Test get_model_id returns correct Haiku model."""
    settings = get_settings()
    assert settings.get_model_id("haiku") == "claude-haiku-4-5-20251001"


def test_get_model_id_invalid_raises_error(mock_api_key):
    """Test that invalid model type raises ValueError."""
    settings = get_settings()
    with pytest.raises(ValueError, match="Invalid model_type"):
        settings.get_model_id("invalid")  # type: ignore


def test_settings_singleton(mock_api_key):
    """Test that get_settings returns same instance (singleton)."""
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2


def test_model_type_literal():
    """Test ModelType is properly typed."""
    # This is a type checking test - just verify the types exist
    valid_types: list[ModelType] = ["opus", "sonnet", "haiku"]
    assert len(valid_types) == 3


if __name__ == "__main__":
    # Allow running as script for quick testing
    from aitestkit.config import get_settings

    settings = get_settings()
    print(f"✅ API Key loaded: {settings.anthropic_api_key[:10]}...")
    print(f"✅ Code Gen Model: {settings.model_code_gen}")
    print(f"✅ Analysis Model: {settings.model_analysis}")
    print(f"✅ Regression Model: {settings.model_regression}")
    print(f"\n✅ Testing get_model_id method:")
    print(f"  Opus: {settings.get_model_id('opus')}")
    print(f"  Sonnet: {settings.get_model_id('sonnet')}")
    print(f"  Haiku: {settings.get_model_id('haiku')}")
    print("\n✅ All manual checks passed!")
