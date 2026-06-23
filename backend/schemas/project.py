from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProjectCreate(BaseModel):
    name: str
    initial_requirement: str


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    initial_requirement: Optional[str] = None
    status: Optional[str] = None


class StepOutputResponse(BaseModel):
    id: UUID
    project_id: UUID
    step: int
    model_key: str
    prompt_template_id: UUID
    display_content: Optional[str]
    has_edited: bool
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def build_display_fields(cls, data: Any) -> Any:
        response_fields = (
            "id",
            "project_id",
            "step",
            "model_key",
            "prompt_template_id",
            "status",
            "created_at",
            "updated_at",
        )

        if isinstance(data, dict):
            values = dict(data)
            ai_output = values.pop("ai_output", None)
            edited_output = values.pop("edited_output", None)
        else:
            values = {
                field: getattr(data, field)
                for field in response_fields
                if hasattr(data, field)
            }
            ai_output = getattr(data, "ai_output", None)
            edited_output = getattr(data, "edited_output", None)

        values["display_content"] = edited_output if edited_output else ai_output
        values["has_edited"] = edited_output is not None and edited_output != ai_output
        return values


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    initial_requirement: str
    current_step: int
    status: str
    created_at: datetime
    updated_at: datetime
    step_outputs: list[StepOutputResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class StepConfigResponse(BaseModel):
    id: UUID
    step: int
    name: str
    brain_type: str
    need_model: bool
    need_terminal: bool
    is_active: bool
    sort_order: int

    model_config = ConfigDict(from_attributes=True)
