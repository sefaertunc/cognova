from cognova.providers.registry import (
    get_provider,
    list_providers,
    register_provider,
    get_provider_tier,
)
from cognova.errors import ProviderNotFoundError
from cognova.providers.base import LLMProvider
import pytest


def test_register_and_get_provider(mock_provider_class):
    register_provider("openai", mock_provider_class, 2)
    provider = get_provider("openai")
    assert isinstance(provider, LLMProvider)


def test_list_providers_empty():
    provider_list = list_providers()
    assert provider_list == []


def test_list_providers_after_registration(mock_provider_class):
    register_provider("openai", mock_provider_class, 2)
    provider_list = list_providers()
    assert len(provider_list) == 1


def test_get_provider_tier_default(mock_provider_class):
    register_provider("sample", mock_provider_class)
    pro_name = get_provider_tier("sample")
    assert pro_name == 3


def test_get_provider_tier_custom(mock_provider_class):
    register_provider("sample", mock_provider_class, 2)
    pro_name = get_provider_tier("sample")
    assert pro_name == 2


def test_get_unknown_provider_raises_error(mock_provider_class):
    with pytest.raises(ProviderNotFoundError):
        get_provider("nonexisting")
