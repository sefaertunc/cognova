"""Framework registry for multi-framework test generation support."""

from cognova.frameworks.registry import (
    FRAMEWORKS,
    FrameworkCategory,
    FrameworkInfo,
    get_core_frameworks,
    get_framework,
    get_framework_choices,
    get_frameworks_by_category,
    list_frameworks,
    validate_framework,
)

__all__ = [
    "FRAMEWORKS",
    "FrameworkCategory",
    "FrameworkInfo",
    "get_core_frameworks",
    "get_framework",
    "get_framework_choices",
    "get_frameworks_by_category",
    "list_frameworks",
    "validate_framework",
]
