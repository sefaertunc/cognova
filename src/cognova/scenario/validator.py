from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


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
    attachments: list[dict[str, Any]] | None = None
    output: str | None = None
