"""
Scenario schema migration.

Migrates scenario YAML files from older schema versions to the current version.

Classes:
- MigrationResult: Dataclass with success, from_version, to_version, changes, backup_path, error

Functions:
- migrate_scenario(path, dry_run, create_backup) -> MigrationResult

Migration behavior:
- Creates backup as *.yaml.bak (unless --no-backup)
- Reports changes made
- Supports --dry-run for preview

See MASTER_SPEC.md Section 7 for schema versioning strategy.

TODO: Implement migrator
"""

# Placeholder - implementation to follow
