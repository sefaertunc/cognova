import pytest
from cognova.scenario.loader import load_scenario_raw
from cognova.scenario.validator import ValidationResult, run_scenario_validation


FULL_SCENARIO = """\
schema_version: 1
target:
  feature: "sample feature"
  component: "auth"
  description: "sample description above 20 chars"
  source_files:
    - sample.py
    - sample2.py
scenarios:
  success:
    - "sample"
    - "sample2"
  failure:
    - "sample"
    - "sample2"
  edge_cases:
    - "sample"
    - "sample2"
test_data:
  valid_example:
    field1: "valid_value"
context:
  - docs/sample.py
framework: "pytest"
attachments:
  - path: src/sample.py
"""

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

INVALID_SCENARIO_DESCRIPTION = """\
schema_version: 1
target:
  feature: "sample feature"
  description: "sample"
scenarios:
  success:
    - "sample"
    - "sample2"
  failure:
    - "sample"
    - "sample2"
"""

INVALID_SCENARIO_TARGET = """\
schema_version: 1
scenarios:
  success:
    - "sample"
    - "sample2"
  failure:
    - "sample"
    - "sample2"
"""

INVALID_SCENARIO_EMPTY = """schema_version: 1"""


def test_run_scenario_validation_valid_scenario_instance(tmp_path):
    (tmp_path / "scenario.yaml").write_text(VALID_SCENARIO)
    scenario_dict = load_scenario_raw(tmp_path / "scenario.yaml")
    val_result = run_scenario_validation(scenario_dict)
    assert isinstance(val_result, ValidationResult)
    assert val_result.is_valid is True


@pytest.mark.parametrize(
    "warning_messages, info_messages",
    [
        ("recommended: target.source_files", "(e.g., auth, api, payment)"),
        ("scenarios.edge_cases", "provided: context"),
        ("coverage: test_data", "available: framework"),
    ],
)
def test_run_scenario_validation_valid_scenario_messages(tmp_path, warning_messages, info_messages):
    (tmp_path / "scenario.yaml").write_text(VALID_SCENARIO)
    scenario_dict = load_scenario_raw(tmp_path / "scenario.yaml")
    val_result = run_scenario_validation(scenario_dict)
    assert any(warning_messages in warn for warn in val_result.warnings)
    assert any(info_messages in inf for inf in val_result.info)


def test_run_scenario_validation_valid_scenario_length(tmp_path):
    (tmp_path / "scenario.yaml").write_text(VALID_SCENARIO)
    scenario_dict = load_scenario_raw(tmp_path / "scenario.yaml")
    val_result = run_scenario_validation(scenario_dict)
    assert len(val_result.errors) == 0
    assert len(val_result.warnings) > 0
    assert len(val_result.info) > 0


def test_run_scenario_validation_full_scenario_length(tmp_path):
    (tmp_path / "scenario.yaml").write_text(FULL_SCENARIO)
    scenario_dict = load_scenario_raw(tmp_path / "scenario.yaml")
    val_result = run_scenario_validation(scenario_dict)
    assert len(val_result.errors) == 0
    assert len(val_result.warnings) == 0
    assert len(val_result.info) == 0


def test_run_scenario_validation_invalid_scenario_target(tmp_path):
    (tmp_path / "scenario.yaml").write_text(INVALID_SCENARIO_TARGET)
    scenario_dict = load_scenario_raw(tmp_path / "scenario.yaml")
    val_result = run_scenario_validation(scenario_dict)
    assert "Missing required section: target" in val_result.errors


def test_run_scenario_validation_invalid_scenario_empty_length(tmp_path):
    (tmp_path / "scenario.yaml").write_text(INVALID_SCENARIO_EMPTY)
    scenario_dict = load_scenario_raw(tmp_path / "scenario.yaml")
    val_result = run_scenario_validation(scenario_dict)
    assert len(val_result.errors) > 0
    assert len(val_result.warnings) > 0
    assert len(val_result.info) > 0


def test_run_scenario_validation_invalid_scenario_empty_description(tmp_path):
    (tmp_path / "scenario.yaml").write_text(INVALID_SCENARIO_DESCRIPTION)
    scenario_dict = load_scenario_raw(tmp_path / "scenario.yaml")
    val_result = run_scenario_validation(scenario_dict)
    assert any("at least 20 characters" in elem for elem in val_result.errors)
