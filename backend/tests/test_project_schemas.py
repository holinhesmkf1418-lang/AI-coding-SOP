from datetime import datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from pydantic import ValidationError

from backend.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    StepConfigResponse,
    StepOutputResponse,
)


def make_step_output(**overrides) -> SimpleNamespace:
    defaults = {
        "id": uuid4(),
        "project_id": uuid4(),
        "step": 1,
        "model_key": "default-model",
        "prompt_template_id": uuid4(),
        "ai_output": "AI output",
        "edited_output": None,
        "status": "generated",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_project_create_requires_name_and_initial_requirement() -> None:
    created = ProjectCreate(name="项目", initial_requirement="需求")

    assert created.name == "项目"
    assert created.initial_requirement == "需求"

    with pytest.raises(ValidationError):
        ProjectCreate(name="项目")


def test_step_output_response_falls_back_to_ai_output_when_edited_output_is_none() -> None:
    response = StepOutputResponse.model_validate(make_step_output())

    assert response.display_content == "AI output"
    assert response.has_edited is False


def test_step_output_response_falls_back_to_ai_output_when_edited_output_is_empty() -> None:
    response = StepOutputResponse.model_validate(make_step_output(edited_output=""))

    assert response.display_content == "AI output"
    assert response.has_edited is True


def test_step_output_response_uses_edited_output_when_present() -> None:
    response = StepOutputResponse.model_validate(make_step_output(edited_output="人工编辑"))

    assert response.display_content == "人工编辑"
    assert response.has_edited is True


def test_project_response_reads_nested_step_outputs_from_attributes() -> None:
    project = SimpleNamespace(
        id=uuid4(),
        name="项目",
        initial_requirement="需求",
        current_step=1,
        status="draft",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        step_outputs=[make_step_output()],
    )

    response = ProjectResponse.model_validate(project)

    assert response.step_outputs[0].display_content == "AI output"


def test_step_config_response_reads_from_attributes() -> None:
    step_config = SimpleNamespace(
        id=uuid4(),
        step=1,
        name="需求完善",
        brain_type="brain",
        need_model=True,
        need_terminal=False,
        is_active=True,
        sort_order=1,
    )

    response = StepConfigResponse.model_validate(step_config)

    assert response.step == 1
    assert response.name == "需求完善"
