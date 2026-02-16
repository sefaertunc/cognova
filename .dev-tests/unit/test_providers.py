import pytest
from cognova.errors import *
from conftest import MockProvider
from cognova.providers.base import (
    TokenUsage,
    LLMResponse,
    LLMProvider,
)


class Incomplete:
    @property
    def name(self):
        return "broken"

    def count_tokens(self, text):
        return len(text.split())


def test_token_usage_creation():
    usage = TokenUsage(input_tokens=0, output_tokens=0)
    assert isinstance(usage, TokenUsage)


def test_token_usage_fields_are_integers():
    usage = TokenUsage(input_tokens=0, output_tokens=0)
    assert isinstance(usage.input_tokens, int)
    assert isinstance(usage.output_tokens, int)


def test_token_usage_creation_with_tokens():
    usage = TokenUsage(input_tokens=100, output_tokens=150)
    assert usage.input_tokens == 100
    assert usage.output_tokens == 150


def test_llm_response_creation():
    usage = TokenUsage(input_tokens=10, output_tokens=10)
    response = LLMResponse(content="hello", model="claude-opus-4.6", usage=usage)
    assert isinstance(response, LLMResponse)
    assert response.content == "hello"
    assert response.model == "claude-opus-4.6"
    assert response.usage is usage


def test_llm_response_empty_content():
    usage = TokenUsage(input_tokens=10, output_tokens=10)
    response = LLMResponse(content="", model="claude-opus-4.6", usage=usage)
    assert response.content == ""


def test_conforming_class_is_llm_provider(mock_provider_class):
    mock = mock_provider_class
    assert isinstance(mock, LLMProvider)


def test_missing_method_is_not_provider():
    incomplete_mock = Incomplete()
    assert not isinstance(incomplete_mock, LLMProvider)
