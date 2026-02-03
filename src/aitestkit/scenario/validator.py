from typing import Any

from pydantic import BaseModel, Field


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
    schema_version: int = 1
    target: TargetConfig
    scenarios: ScenariosConfig
    test_data: dict[str, Any] | None = None
    context: list[str] | None = None
    attachments: list[dict[str, Any]] | None = None
