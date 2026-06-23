from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel


class PromptTemplate(SQLModel, table=True):
    __tablename__ = "prompt_templates"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    step: int = Field(sa_column=Column(Integer, nullable=False))
    name: str = Field(sa_column=Column(String(100), nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
    is_default: bool = Field(
        default=True,
        sa_column=Column(
            Boolean,
            nullable=False,
            server_default="1",
        ),
    )
    is_custom: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
            server_default="0",
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
