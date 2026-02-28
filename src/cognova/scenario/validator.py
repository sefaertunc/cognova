from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from cognova.scenario.loader import Attachment


class TargetConfig(BaseModel):
    feature: str
    description: str = Field(min_length=20)
    component: str | None = None
    source_files: list[str] | None = None


class ScenariosConfig(BaseModel):
    success: list[str]
    failure: list[str]
    edge_cases: list[str] | None = None


class ScenarioFile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_version: int = 1
    target: TargetConfig
    scenarios: ScenariosConfig
    quality: Literal["standard", "high"] = "standard"
    edge_cases_enabled: bool = Field(default=False, alias="edge_cases")
    fault_analysis: bool = False
    framework: str | None = None
    test_data: dict[str, Any] | None = None
    context: list[str] | None = None
    attachments: list[Attachment] | None = None
    output: str | None = None


@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)


def run_scenario_validation(data: dict[str, Any]) -> ValidationResult:
    """Validate scenario dict with three-tier checks (errors/warnings/info)."""
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    # --- Required (errors) ---
    target = data.get("target")
    if not isinstance(target, dict):
        errors.append("Missing required section: target")
    else:
        if not target.get("feature"):
            errors.append("target.feature is required (e.g., User Login, Shopping Cart)")
        desc = target.get("description", "")
        if len(desc) < 20:
            errors.append("target.description must be at least 20 characters")
        if not target.get("source_files"):
            warnings.append("Providing source files is recommended: target.source_files")
        if not target.get("component"):
            info.append("Component identifier: target.component (e.g., auth, api, payment)")

    scenarios = data.get("scenarios")
    if not isinstance(scenarios, dict):
        errors.append("Missing required section: scenarios")
    else:
        if not scenarios.get("success"):
            errors.append("scenarios.success must have at least 1 entry")
        if not scenarios.get("failure"):
            errors.append("scenarios.failure must have at least 1 entry")
        if not scenarios.get("edge_cases"):
            warnings.append("Edge cases recommended: scenarios.edge_cases")

    # --- Recommended (warnings) ---
    if not data.get("test_data"):
        warnings.append("Test data improves scenario coverage: test_data")

    # --- Optional (info) ---
    if not data.get("context"):
        info.append("Additional context files can be provided: context")
    if not data.get("framework"):
        info.append("Framework override available: framework")
    if not data.get("attachments"):
        info.append("File attachments available for richer context: attachments")

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        info=info,
    )
