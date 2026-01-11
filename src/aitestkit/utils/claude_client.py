from dataclasses import dataclass

from anthropic import Anthropic
from anthropic.types import TextBlock

from aitestkit.config import ModelType, Settings, get_settings


@dataclass
class UsageStats:
    """Data class to hold usage statistics from Claude API responses."""

    input_tokens: int = 0
    output_tokens: int = 0
    api_calls: int = 0

    # Pricing per 1M tokens (as of January 2025)
    # Source: https://www.anthropic.com/pricing
    PRICING = {
        "opus": {"input": 5.00, "output": 25.00},  # Claude Opus 4.5
        "sonnet": {"input": 3.00, "output": 15.00},  # Claude Sonnet 4.5
        "haiku": {"input": 1.00, "output": 5.00},  # Claude Haiku 4.5
    }

    @property
    def estimated_cost(self) -> float:
        """Calculate estimated cost in USD based on average pricing.

        Returns:
            Total estimated cost based on token usage and pricing

        Note:
            Uses average pricing across all models. For per-model cost,
            multiply tokens by specific model pricing from PRICING dict.
        """
        # Cost = (tokens / 1M) * price_per_1M
        # Using average across Opus 4.5, Sonnet 4.5, and Haiku 4.5
        avg_input_price = (5.00 + 3.00 + 1.00) / 3
        avg_output_price = (25.00 + 15.00 + 5.00) / 3
        input_cost = (self.input_tokens / 1_000_000) * avg_input_price
        output_cost = (self.output_tokens / 1_000_000) * avg_output_price
        return input_cost + output_cost

    def __add__(self, other: "UsageStats") -> "UsageStats":
        """Combine usage statistics from multiple instances."""
        return UsageStats(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            api_calls=self.api_calls + other.api_calls,
        )


class ClaudeClient:
    """Client for interacting with the Anthropic Claude API."""

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()
        self._client = Anthropic(api_key=self._settings.anthropic_api_key)
        self._usage: dict[str, UsageStats] = {
            "opus": UsageStats(),
            "sonnet": UsageStats(),
            "haiku": UsageStats(),
        }

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model_type: ModelType = "sonnet",
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        """Generate a response from the Claude API.

        Args:
            system_prompt: The system prompt to set context.
            user_prompt: The user prompt for the model to respond to.
            model_type: The type of model to use ("opus", "sonnet", or "haiku").
            max_tokens: Maximum tokens for the response.
            temperature: Sampling temperature for generation.
        Returns:
            The generated response text.
        """
        model_id = self._settings.get_model_id(model_type)
        response = self._client.messages.create(
            model=model_id,
            max_tokens=max_tokens or self._settings.max_tokens,
            temperature=temperature if temperature is not None else self._settings.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        # Update usage statistics
        usage = self._usage[model_type]
        usage.input_tokens += response.usage.input_tokens
        usage.output_tokens += response.usage.output_tokens
        usage.api_calls += 1

        # Extract text from response (assuming first content block is text)
        content_block = response.content[0]
        if isinstance(content_block, TextBlock):
            return content_block.text
        else:
            raise ValueError(f"Unexpected content block type: {type(content_block)}")

    def generate_code(self, system_prompt: str, user_prompt: str) -> str:
        """Generate code using Opus (highest quality).

        Args:
            system_prompt: The system prompt to set context.
            user_prompt: Code generation request.

        Returns:
            The generated code as a string.
        """
        return self.generate(
            system_prompt=system_prompt, user_prompt=user_prompt, model_type="opus", temperature=0.2
        )

    def analyze(self, system_prompt: str, user_prompt: str) -> str:
        """Analyze content using Sonnet (balanced quality/cost).

        Args:
            system_prompt: The system prompt to set context.
            user_prompt: Content to analyze.

        Returns:
            The analysis result as a string.
        """
        return self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model_type="sonnet",
            temperature=0.4,
        )

    def quick_check(self, system_prompt: str, user_prompt: str) -> str:
        """Quick validation using Haiku (fast and cheap).

        Args:
            system_prompt: The system prompt to set context.
            user_prompt: Content to validate.

        Returns:
            The validation result as a string.
        """
        return self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model_type="haiku",
            temperature=0.2,
        )

    def get_usage(self, model_type: ModelType | None = None) -> UsageStats:
        """Retrieve usage statistics.

        Args:
            model_type: Specific model to get stats for, or None for total.

        Returns:
            UsageStats object for specified model or combined total.
        """
        if model_type is not None:
            return self._usage[model_type]

        # Return combined stats for all models
        total = UsageStats()
        for stats in self._usage.values():
            total = total + stats
        return total

    def get_total_cost(self) -> float:
        """Calculate total estimated cost across all model types.

        Returns:
            Total cost in USD.
        """
        total = 0.0
        for usage in self._usage.values():
            total += usage.estimated_cost
        return total

    def reset_usage(self) -> None:
        """Reset usage statistics for all model types to zero."""
        self._usage = {"opus": UsageStats(), "sonnet": UsageStats(), "haiku": UsageStats()}
