from pathlib import Path

import pytest
import yaml

from conftest import VALID_SCENARIO

from cognova.errors import ScenarioValidationError
from cognova.scenario.migrator import (
    detect_version,
    check_schema_version,
    migrate_scenario,
    migrate_v0_to_v1,
    CURRENT_SCHEMA_VERSION,
)


def test_detect_version_with_version():
    data = yaml.safe_load(VALID_SCENARIO)
    version = detect_version(data)
    assert version == CURRENT_SCHEMA_VERSION


def test_detect_version_with_empty_dict():
    version = detect_version({})
    assert version == 0


def test_check_schema_version_current_version():
    data = yaml.safe_load(VALID_SCENARIO)
    warnings = check_schema_version(data=data, file=Path("valid.yaml"))
    assert warnings == []


def test_check_schema_version_unsupported(monkeypatch):
    data = yaml.safe_load(VALID_SCENARIO)
    monkeypatch.setattr("cognova.scenario.migrator.UNSUPPORTED_VERSIONS", [1])
    with pytest.raises(ScenarioValidationError):
        check_schema_version(data=data, file=Path("valid.yaml"))


def test_check_schema_version_deprecated(monkeypatch):
    data = yaml.safe_load(VALID_SCENARIO)
    monkeypatch.setattr("cognova.scenario.migrator.DEPRECATED_VERSIONS", [1])
    warnings = check_schema_version(data=data, file=Path("valid.yaml"))
    assert any("deprecated" in warn for warn in warnings)


def test_migrate_v0_to_v1(monkeypatch):
    monkeypatch.setattr("cognova.scenario.migrator.CURRENT_SCHEMA_VERSION", 2)
    data, changes = migrate_v0_to_v1({})
    assert data["schema_version"] == 2
    assert len(changes) == 1


def test_migrate_v0_to_v1_already_has_version():
    data = yaml.safe_load(VALID_SCENARIO)
    result, changes = migrate_v0_to_v1(data)
    assert result["schema_version"] == CURRENT_SCHEMA_VERSION
    assert changes == []


def test_migrate_scenario_same_version(tmp_path):
    scenario = tmp_path / "scenario.yaml"
    (scenario).write_text(VALID_SCENARIO)
    result = migrate_scenario(path=scenario)
    assert result.migrated is False


def test_migrate_scenario_unsupported_version(tmp_path, monkeypatch):
    monkeypatch.setattr("cognova.scenario.migrator.CURRENT_SCHEMA_VERSION", 2)
    monkeypatch.setattr("cognova.scenario.migrator.UNSUPPORTED_VERSIONS", [1])
    scenario = tmp_path / "scenario.yaml"
    (scenario).write_text(VALID_SCENARIO)
    with pytest.raises(ScenarioValidationError):
        result = migrate_scenario(path=scenario)


def test_migrate_scenario_migration(tmp_path, monkeypatch):
    monkeypatch.setattr("cognova.scenario.migrator.CURRENT_SCHEMA_VERSION", 2)
    monkeypatch.setattr("cognova.scenario.migrator.DEPRECATED_VERSIONS", [1])
    scenario = tmp_path / "scenario.yaml"
    (scenario).write_text(VALID_SCENARIO)
    result = migrate_scenario(path=scenario)
    assert result.to_version == 2


def test_migrate_scenario_migration_with_backup(tmp_path, monkeypatch):
    monkeypatch.setattr("cognova.scenario.migrator.CURRENT_SCHEMA_VERSION", 2)
    monkeypatch.setattr("cognova.scenario.migrator.DEPRECATED_VERSIONS", [1])
    scenario = tmp_path / "scenario.yaml"
    (scenario).write_text(VALID_SCENARIO)
    result = migrate_scenario(path=scenario, create_backup=True)
    assert (tmp_path / "scenario.yaml.bak").is_file()


def test_migrate_scenario_no_backup(tmp_path, monkeypatch):
    monkeypatch.setattr("cognova.scenario.migrator.CURRENT_SCHEMA_VERSION", 2)
    scenario = tmp_path / "scenario.yaml"
    scenario.write_text(VALID_SCENARIO)
    migrate_scenario(path=scenario, create_backup=False)
    assert not (tmp_path / "scenario.yaml.bak").exists()


def test_migrate_scenario_migration_with_dry_run(tmp_path, monkeypatch):
    monkeypatch.setattr("cognova.scenario.migrator.CURRENT_SCHEMA_VERSION", 2)
    scenario = tmp_path / "scenario.yaml"
    scenario.write_text(VALID_SCENARIO)
    original_content = scenario.read_text()
    result = migrate_scenario(path=scenario, dry_run=True)
    assert result.to_version == 2
    assert scenario.read_text() == original_content
