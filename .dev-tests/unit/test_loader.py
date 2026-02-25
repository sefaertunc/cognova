import pytest

from cognova.errors import ScenarioLoadError, ScenarioValidationError
from cognova.scenario.loader import detect_language, load_scenario, load_scenario_raw
from cognova.scenario.validator import ScenarioFile

VALID_SCENARIO = """\
schema_version: 1
target:
  feature: "sample feature"
  description: "sample description above 20 chars"
scenarios:
  success:
    - "sample"
    - "sample2"
  failure:
    - "sample"
    - "sample2"
"""

INVALID_SCENARIO = """\
schema_version: 1
target:
  feature: "sample feature"
  description: "sample description"
scenarios:
  success:
    - "sample"
    - "sample2"
  failure:
    - "sample"
    - "sample2"
"""


@pytest.mark.parametrize(
    ("extension", "language"),
    [("py", "python"), ("js", "javascript"), ("cs", "csharp"), ("sh", "bash")],
)
def test_detect_language(extension, language):
    assert detect_language(f"sample.{extension}") == language


def test_detect_language_unknown_extension():
    assert detect_language("file.xyz") == "text"


def test_load_scenario_raw_valid(tmp_path):
    (tmp_path / "scenario.yaml").write_text(VALID_SCENARIO)
    result = load_scenario_raw(tmp_path / "scenario.yaml")
    assert isinstance(result, dict)
    assert "schema_version" in result
    assert "target" in result
    assert "scenarios" in result


def test_load_scenario_raw_file_not_found(tmp_path):
    with pytest.raises(ScenarioLoadError, match="File not found"):
        load_scenario_raw(tmp_path / "not_existing.yaml")


def test_load_scenario_raw_invalid_yaml(tmp_path):
    (tmp_path / "scenario.yaml").write_text("invalid_yaml: [unclosed_list")
    with pytest.raises(ScenarioLoadError, match="Invalid YAML"):
        load_scenario_raw(tmp_path / "scenario.yaml")


def test_load_scenario_raw_not_dict(tmp_path):
    (tmp_path / "scenario.yaml").write_text("- just a list")
    with pytest.raises(ScenarioLoadError, match="YAML mapping"):
        load_scenario_raw(tmp_path / "scenario.yaml")


def test_load_scenario_valid_path_instance(tmp_path):
    (tmp_path / "scenario.yaml").write_text(VALID_SCENARIO)
    result = load_scenario(tmp_path / "scenario.yaml")
    assert isinstance(result, ScenarioFile)


def test_load_scenario_valid_scenario(tmp_path):
    (tmp_path / "scenario.yaml").write_text(VALID_SCENARIO)
    result = load_scenario(tmp_path / "scenario.yaml")
    assert result.schema_version == 1
    assert result.target.feature == "sample feature"
    assert result.quality == "standard"


def test_load_scenario_invalid_scenario(tmp_path):
    (tmp_path / "scenario.yaml").write_text(INVALID_SCENARIO)
    with pytest.raises(ScenarioValidationError, match="validation failed"):
        load_scenario(tmp_path / "scenario.yaml")
