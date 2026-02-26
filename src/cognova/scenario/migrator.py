"""
Scenario schema migration.

Migrates scenario YAML files from older schema versions to the current version.
Creates backups, reports changes, and supports dry-run preview.
"""

from dataclasses import dataclass, field
from pathlib import Path
from shutil import copy2
from typing import Any

import yaml

from cognova.errors import ScenarioValidationError
from cognova.scenario.loader import load_scenario_raw

CURRENT_SCHEMA_VERSION = 1
DEPRECATED_VERSIONS: list[int] = []
UNSUPPORTED_VERSIONS: list[int] = []


@dataclass
class MigrationResult:
    migrated: bool = False
    from_version: int = 0
    to_version: int = CURRENT_SCHEMA_VERSION
    changes: list[str] = field(default_factory=list)
    backup_path: str | None = None


def detect_version(data: dict[str, Any]) -> int:
    """Return schema_version from scenario dict, defaults to 0 if missing."""
    return int(data.get("schema_version", 0))


def check_schema_version(data: dict[str, Any], file: Path) -> list[str]:
    """Return deprecation warnings; raise ScenarioValidationError for unsupported versions."""
    warnings: list[str] = []
    version = detect_version(data)
    if version in UNSUPPORTED_VERSIONS:
        raise ScenarioValidationError(
            file=file,
            errors=[
                f"Schema version {version} is no longer supported",
                f"Run migrate_scenario to update {file}",
            ],
        )
    if version in DEPRECATED_VERSIONS:
        warnings.append(
            f"Schema version {version} is deprecated. "
            f"Will stop working in v{CURRENT_SCHEMA_VERSION + 1}. "
            f"Use migrate_scenario to update."
        )
    return warnings


def migrate_v0_to_v1(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Add schema_version: 1 to a v0 scenario dict."""
    migrated = dict(data)
    changes: list[str] = []
    if "schema_version" not in migrated:
        migrated["schema_version"] = CURRENT_SCHEMA_VERSION
        changes.append(f"Added schema_version: {CURRENT_SCHEMA_VERSION}")
    return (migrated, changes)


def migrate_scenario(
    path: Path, dry_run: bool = False, create_backup: bool = True
) -> MigrationResult:
    """Migrate scenario YAML file to current schema version."""
    data = load_scenario_raw(path=path)
    file_version = detect_version(data)

    if file_version == CURRENT_SCHEMA_VERSION:
        return MigrationResult(
            migrated=False, from_version=file_version, to_version=file_version
        )

    if file_version in UNSUPPORTED_VERSIONS:
        raise ScenarioValidationError(
            file=path,
            errors=[f"Schema version {file_version} is no longer supported"],
        )
    changes: list[str] = []
    if file_version < CURRENT_SCHEMA_VERSION:
        data, changes = migrate_v0_to_v1(data)

    if dry_run:
        return MigrationResult(
            migrated=True,
            from_version=file_version,
            to_version=CURRENT_SCHEMA_VERSION,
            changes=changes,
        )

    backup_path: str | None = None
    if create_backup:
        bak = Path(f"{path}.bak")
        copy2(path, bak)
        backup_path = str(bak)

    with open(path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

    return MigrationResult(
        migrated=True,
        from_version=file_version,
        to_version=CURRENT_SCHEMA_VERSION,
        changes=changes,
        backup_path=backup_path,
    )
