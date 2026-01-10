"""Shared test fixtures and utilities."""

from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_test_data_dir() -> Path:
    """Get the test data directory."""
    return Path(__file__).parent / "test_data"
