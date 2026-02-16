import pydantic
import pytest
import yaml
from cognova.config import (
    get_settings,
    Settings,
    ProductConfig,
    DefaultsConfig,
    GenerationConfig,
    ModelsConfig,
    ProjectConfig,
    QualityTiersConfig,
    RepairConfig,
    SelfHealingConfig,
    ContextConfig,
    EmbeddingsConfig,
    load_project_config,
    SONNET_MODEL,
    OPUS_MODEL,
    HAIKU_MODEL,
)


def test_settings_loads_from_env(mock_api_key):
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.anthropic_api_key == "test-key-12345"


def test_settings_singleton(mock_api_key):
    get_settings.cache_clear()
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2


def test_missing_api_key_raises_validation_error(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    get_settings.cache_clear()
    with pytest.raises(Exception) as exc_info:
        get_settings()
    assert "field required" in str(exc_info.value).lower()


@pytest.mark.parametrize(
    "product_name,product_type,tech_stack",
    [
        ("TestProduct", "cli", ["python", "docker"]),
        ("AnotherProduct", "web_app", ["javascript", "nodejs"]),
        ("MobileApp", "mobile", ["flutter", "dart"]),
        ("DesktopApp", "desktop", ["electron", "react"]),
        ("APIService", "api", ["go", "kubernetes"]),
    ],
)
def test_production_config_initialization(product_name, product_type, tech_stack):
    production = ProductConfig(name=product_name, type=product_type, tech_stack=tech_stack)
    assert isinstance(production, ProductConfig)
    assert isinstance(production.name, str)
    assert isinstance(production.type, str)
    assert isinstance(production.tech_stack, list)


@pytest.mark.parametrize(
    "invalid_name,invalid_type,invalid_tech",
    [
        (123, "invalid", ["python", 456]),
        (None, None, [None, None]),
        ("valid_name", "cli", [123, "web"]),
        ("valid_name", "invalid_type", ["python", "docker"]),
        (1234, "web_app", ["python", "docker"]),
    ],
)
def test_product_config_invalid_initialization(invalid_name, invalid_type, invalid_tech):
    with pytest.raises(pydantic.ValidationError):
        ProductConfig(
            name=invalid_name,
            type=invalid_type,  # type: ignore
            tech_stack=invalid_tech,  # type: ignore
        )


def test_defaults_config_initialization():
    defaults = DefaultsConfig()
    assert isinstance(defaults, DefaultsConfig)


def test_defaults_config_default_values():
    defaults = DefaultsConfig()
    assert defaults.framework == "pytest"
    assert defaults.output_dir == "tests/generated"


@pytest.mark.parametrize(
    "invalid_framework,invalid_output_dir",
    [
        (123, "tests/generated"),
        ("pytest", 456),
        (None, None),
        ([], "tests/generated"),
        ("pytest", {}),
    ],
)
def test_defaults_config_invalid_initialization(invalid_framework, invalid_output_dir):
    with pytest.raises(pydantic.ValidationError):
        defaults = DefaultsConfig(framework=invalid_framework, output_dir=invalid_output_dir)  # type: ignore


def test_generation_config_initialization():
    generation = GenerationConfig()
    assert isinstance(generation, GenerationConfig)


def test_generation_config_default_values():
    generation = GenerationConfig()
    assert generation.warn_after_n == 10


@pytest.mark.parametrize(
    "invalid_warn_after_n",
    ["ten", None, 3.5, [], {}],
)
def test_generation_config_invalid_initialization(invalid_warn_after_n):
    with pytest.raises(pydantic.ValidationError):
        GenerationConfig(warn_after_n=invalid_warn_after_n)  # type: ignore


def test_models_config_initialization():
    models = ModelsConfig()
    assert isinstance(models, ModelsConfig)


def test_models_config_default_values():
    models = ModelsConfig()
    assert models.generation == SONNET_MODEL
    assert models.analysis == SONNET_MODEL
    assert models.validation == HAIKU_MODEL


def test_quality_tiers_default_values():
    tiers = QualityTiersConfig()
    assert tiers.standard.generation == SONNET_MODEL
    assert tiers.high.generation == OPUS_MODEL


def test_repair_config_defaults():
    repair = RepairConfig()
    assert repair.max_attempts == 3
    assert repair.cost_cap_usd == 0.50


def test_self_healing_config_defaults():
    healing = SelfHealingConfig()
    assert healing.mode == "suggest"


def test_context_config_defaults():
    context = ContextConfig()
    assert context.auto_init is True
    assert "python" in context.languages


def test_embeddings_config_defaults():
    embeddings = EmbeddingsConfig()
    assert "MiniLM" in embeddings.text_model
    assert "unixcoder" in embeddings.code_model


def test_project_config_get_model_for_role_generation_standard():
    config = ProjectConfig()
    assert config.get_model_for_role("generation", "standard") == SONNET_MODEL


def test_project_config_get_model_for_role_generation_high():
    config = ProjectConfig()
    assert config.get_model_for_role("generation", "high") == OPUS_MODEL


def test_project_config_get_model_for_role_analysis():
    config = ProjectConfig()
    assert config.get_model_for_role("analysis") == SONNET_MODEL


def test_project_config_get_model_for_role_validation():
    config = ProjectConfig()
    assert config.get_model_for_role("validation") == HAIKU_MODEL


def test_project_config_get_model_for_role_invalid():
    config = ProjectConfig()
    with pytest.raises(ValueError, match="Unknown role"):
        config.get_model_for_role("invalid_role")


def test_load_project_config_no_file(tmp_path):
    result = load_project_config(tmp_path)
    assert result is None


def test_load_project_config_uses_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = load_project_config(None)
    assert result is None


def test_load_project_config_valid_minimal(tmp_path):
    config_dir = tmp_path / ".cognova"
    config_dir.mkdir()
    (config_dir / "config.yaml").write_text(
        """
        schema_version: "4.0"
        product:
          name: TestProduct
          type: cli
          tech_stack: [python, docker]
          """
    )
    result = load_project_config(tmp_path)
    assert result is not None
    assert result.product.name == "TestProduct"
    assert result.defaults.framework == "pytest"


def test_load_project_config_empty_yaml(tmp_path):
    config_dir = tmp_path / ".cognova"
    config_dir.mkdir()
    (config_dir / "config.yaml").write_text("")
    result = load_project_config(tmp_path)
    assert result is None


def test_load_project_config_invalid_yaml(tmp_path):
    config_dir = tmp_path / ".cognova"
    config_dir.mkdir()
    (config_dir / "config.yaml").write_text("invalid_yaml: [unclosed_list")
    with pytest.raises(yaml.YAMLError):
        load_project_config(tmp_path)


def test_load_project_config_invalid_data_types(tmp_path):
    config_dir = tmp_path / ".cognova"
    config_dir.mkdir()
    (config_dir / "config.yaml").write_text(
        """
        schema_version: "one"
        product:
          name: 123
          type: invalid_type
        """
    )
    with pytest.raises(pydantic.ValidationError):
        load_project_config(tmp_path)
