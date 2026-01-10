from pathlib import Path
from typing import Literal
import functools

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Model ID constants
OPUS_MODEL = "claude-opus-4-5-20251101"
SONNET_MODEL = "claude-sonnet-4-5-20250929"
HAIKU_MODEL = "claude-haiku-4-5-20251001"

# Type alias for model selection
ModelType = Literal["opus", "sonnet", "haiku"]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AITESTKIT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra ="ignore"
    )
    anthropic_api_key: str = Field(..., validation_alias="ANTHROPIC_API_KEY")
    model_code_gen: str = OPUS_MODEL
    model_analysis: str = SONNET_MODEL
    model_regression: str = HAIKU_MODEL
    max_tokens: int = 4096
    temperature: float = 0.3
    output_dir: Path = Path("./generated")

    def get_model_id(self, model_type: ModelType) -> str:
        """Get the model ID for the specified model type.

        Args:
            model_type: The type of model ("opus", "sonnet", or "haiku")

        Returns:
            The full model ID string

        Raises:
            ValueError: If model_type is invalid
        """
        mapping = {
            "opus": self.model_code_gen,
            "sonnet": self.model_analysis,
            "haiku": self.model_regression,
        }

        if model_type not in mapping:
            raise ValueError(
                f"Invalid model_type: {model_type}. "
                f"Must be one of: {list(mapping.keys())}"
            )

        return mapping[model_type]


@functools.lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Uses LRU cache to ensure only one Settings instance is created.
    This prevents multiple reads of .env file.
    """
    return Settings()