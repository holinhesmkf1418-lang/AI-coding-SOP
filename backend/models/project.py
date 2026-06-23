from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel


FIRST_STEP = 1
PROJECT_STATUS_DEFAULT = "draft"
STEP_OUTPUT_STATUS_DEFAULT = "pending"


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(sa_column=Column(String(100), nullable=False))
    initial_requirement: str = Field(sa_column=Column(Text, nullable=False))
    current_step: int = Field(
        default=FIRST_STEP,
        sa_column=Column(
            Integer,
            nullable=False,
            server_default=str(FIRST_STEP),
        ),
    )
    status: str = Field(
        default=PROJECT_STATUS_DEFAULT,
        sa_column=Column(
            String(20),
            nullable=False,
            server_default=PROJECT_STATUS_DEFAULT,
        ),
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=func.current_timestamp(),
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=func.current_timestamp(),
            onupdate=datetime.utcnow,
        ),
    )


class StepOutput(SQLModel, table=True):
    __tablename__ = "step_outputs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    project_id: UUID = Field(
        sa_column=Column(
            ForeignKey("projects.id"),
            nullable=False,
        ),
    )
    step: int = Field(sa_column=Column(Integer, nullable=False))
    model_key: str = Field(sa_column=Column(String(50), nullable=False))
    prompt_template_id: UUID = Field(nullable=False)
    ai_output: Optional[str] = Field(default=None, sa_column=Column(Text))
    edited_output: Optional[str] = Field(default=None, sa_column=Column(Text))
    human_edit_diff: Optional[str] = Field(default=None, sa_column=Column(Text))
    status: str = Field(
        default=STEP_OUTPUT_STATUS_DEFAULT,
        sa_column=Column(
            String(20),
            nullable=False,
            server_default=STEP_OUTPUT_STATUS_DEFAULT,
        ),
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=func.current_timestamp(),
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=func.current_timestamp(),
            onupdate=datetime.utcnow,
        ),
    )
