from pathlib import Path
from typing import Literal
import functools

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

SONNET_MODEL = "claude-sonnet-4-5-20250514"
OPUS_MODEL = "claude-opus-4-6"
HAIKU_MODEL = "claude-haiku-4-5-20250514"

ModelType = Literal["opus", "sonnet", "haiku"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="COGNOVA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    anthropic_api_key: str = Field(..., validation_alias="ANTHROPIC_API_KEY")
    log_level: str = "INFO"


@functools.lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


class QualityTierConfig(BaseModel):
    """Quality tier model selection."""

    generation: str = SONNET_MODEL


class QualityTiersConfig(BaseModel):
    """Standard and high quality presets."""

    standard: QualityTierConfig = QualityTierConfig(generation=SONNET_MODEL)
    high: QualityTierConfig = QualityTierConfig(generation=OPUS_MODEL)


class ModelsConfig(BaseModel):
    """Model configuration by role."""

    generation: str = SONNET_MODEL
    analysis: str = SONNET_MODEL
    validation: str = HAIKU_MODEL


class RepairConfig(BaseModel):
    """Repair loop configuration."""

    max_attempts: int = 3
    cost_cap_usd: float = 0.50


class SelfHealingConfig(BaseModel):
    """Self-healing mode configuration."""

    mode: Literal["off", "suggest", "auto"] = "suggest"


class ContextConfig(BaseModel):
    """Project context analysis configuration."""

    auto_init: bool = True
    languages: list[str] = ["python", "typescript"]


class EmbeddingsConfig(BaseModel):
    """Embedding model configuration."""

    text_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    code_model: str = "microsoft/unixcoder-base-nine"


class ProductConfig(BaseModel):
    """Product-level configuration."""

    name: str
    type: Literal["web_app", "api", "desktop", "mobile", "cli"] = "web_app"
    tech_stack: list[str] = []


class DefaultsConfig(BaseModel):
    """Default settings for generation."""

    framework: str = "pytest"
    output_dir: str = "tests/generated"


class GenerationConfig(BaseModel):
    """Generation behavior configuration."""

    warn_after_n: int = 10


class ProjectConfig(BaseModel):
    """Project-level configuration from .cognova/config.yaml."""

    schema_version: str = "4.0"
    product: ProductConfig | None = None
    defaults: DefaultsConfig = DefaultsConfig()
    generation: GenerationConfig = GenerationConfig()
    models: ModelsConfig = ModelsConfig()
    quality_tiers: QualityTiersConfig = QualityTiersConfig()
    repair: RepairConfig = RepairConfig()
    self_healing: SelfHealingConfig = SelfHealingConfig()
    context: ContextConfig = ContextConfig()
    embeddings: EmbeddingsConfig = EmbeddingsConfig()

    def get_model_for_role(self, role: str, quality: str = "standard") -> str:
        """Resolve model ID by role and quality tier.

        Args:
            role: "generation", "analysis", or "validation"
            quality: "standard" or "high"

        Returns:
            Model ID string
        """
        if role == "generation":
            tier = getattr(self.quality_tiers, quality, self.quality_tiers.standard)
            return tier.generation
        mapping = {
            "analysis": self.models.analysis,
            "validation": self.models.validation,
        }
        if role not in mapping:
            raise ValueError(f"Unknown role: {role}. Must be: generation, analysis, validation")
        return mapping[role]


def load_project_config(project_root: Path | None = None) -> ProjectConfig | None:
    """Load project configuration from .cognova/config.yaml.

    Args:
        project_root: Root directory of the project. If None, uses current directory.

    Returns:
        ProjectConfig if file exists and is valid, None otherwise.
    """
    if project_root is None:
        project_root = Path.cwd()

    config_path = project_root / ".cognova" / "config.yaml"
    if not config_path.exists():
        return None

    with config_path.open() as f:
        data = yaml.safe_load(f)

    return ProjectConfig(**data) if data else None
