"""create projects and step outputs

Revision ID: 20260623_0001
Revises:
Create Date: 2026-06-23 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260623_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("initial_requirement", sa.Text(), nullable=False),
        sa.Column("current_step", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="draft", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "step_outputs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("step", sa.Integer(), nullable=False),
        sa.Column("model_key", sa.String(length=50), nullable=False),
        sa.Column("prompt_template_id", sa.Uuid(), nullable=False),
        sa.Column("ai_output", sa.Text(), nullable=True),
        sa.Column("edited_output", sa.Text(), nullable=True),
        sa.Column("human_edit_diff", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="pending", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("step_outputs")
    op.drop_table("projects")
