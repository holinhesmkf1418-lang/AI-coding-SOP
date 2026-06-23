import os
import sqlite3
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALEMBIC_CONFIG = PROJECT_ROOT / "backend" / "alembic.ini"
PROMPT_TEMPLATE_SEED = PROJECT_ROOT / "backend" / "seed_prompt_templates.py"


def run_alembic_upgrade(database_url: str) -> None:
    environment = os.environ.copy()
    environment["DATABASE_URL"] = database_url

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            str(ALEMBIC_CONFIG),
            "upgrade",
            "head",
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def run_prompt_template_seed(database_url: str) -> None:
    environment = os.environ.copy()
    environment["DATABASE_URL"] = database_url

    result = subprocess.run(
        [sys.executable, str(PROMPT_TEMPLATE_SEED)],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def table_columns(connection: sqlite3.Connection, table_name: str) -> dict[str, sqlite3.Row]:
    return {
        row["name"]: row
        for row in connection.execute(f'PRAGMA table_info("{table_name}")').fetchall()
    }


def test_alembic_upgrade_creates_phase1_tables(tmp_path: Path) -> None:
    database_path = tmp_path / "app.db"
    database_url = f"sqlite:///{database_path}"
    run_alembic_upgrade(database_url)
    run_alembic_upgrade(database_url)

    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row

        projects = table_columns(connection, "projects")
        step_outputs = table_columns(connection, "step_outputs")
        prompt_templates = table_columns(connection, "prompt_templates")
        foreign_keys = connection.execute('PRAGMA foreign_key_list("step_outputs")').fetchall()
        journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
        versions = [
            row["version_num"]
            for row in connection.execute("SELECT version_num FROM alembic_version").fetchall()
        ]

    assert set(projects) == {
        "id",
        "name",
        "initial_requirement",
        "current_step",
        "status",
        "created_at",
        "updated_at",
    }
    assert projects["name"]["type"] == "VARCHAR(100)"
    assert projects["initial_requirement"]["type"] == "TEXT"
    assert projects["current_step"]["type"] == "INTEGER"
    assert projects["current_step"]["dflt_value"] == "1"
    assert projects["status"]["type"] == "VARCHAR(20)"
    assert projects["status"]["dflt_value"] == "'draft'"

    assert set(step_outputs) == {
        "id",
        "project_id",
        "step",
        "model_key",
        "prompt_template_id",
        "ai_output",
        "edited_output",
        "human_edit_diff",
        "status",
        "created_at",
        "updated_at",
    }
    assert step_outputs["step"]["type"] == "INTEGER"
    assert step_outputs["model_key"]["type"] == "VARCHAR(50)"
    assert step_outputs["ai_output"]["type"] == "TEXT"
    assert step_outputs["edited_output"]["type"] == "TEXT"
    assert step_outputs["human_edit_diff"]["type"] == "TEXT"
    assert step_outputs["status"]["type"] == "VARCHAR(20)"
    assert step_outputs["status"]["dflt_value"] == "'pending'"

    assert [
        {
            "from": row["from"],
            "table": row["table"],
            "to": row["to"],
        }
        for row in foreign_keys
    ] == [{"from": "project_id", "table": "projects", "to": "id"}]
    assert journal_mode == "wal"
    assert set(prompt_templates) == {
        "id",
        "step",
        "name",
        "content",
        "is_default",
        "is_custom",
        "created_at",
    }
    assert prompt_templates["step"]["type"] == "INTEGER"
    assert prompt_templates["name"]["type"] == "VARCHAR(100)"
    assert prompt_templates["content"]["type"] == "TEXT"
    assert prompt_templates["is_default"]["dflt_value"] == "1"
    assert prompt_templates["is_custom"]["dflt_value"] == "0"

    assert journal_mode == "wal"
    assert versions == ["20260623_0002"]


def test_prompt_template_seed_is_repeatable(tmp_path: Path) -> None:
    database_path = tmp_path / "app.db"
    database_url = f"sqlite:///{database_path}"
    run_alembic_upgrade(database_url)
    run_prompt_template_seed(database_url)
    run_prompt_template_seed(database_url)

    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT step, name, content, is_default, is_custom
            FROM prompt_templates
            ORDER BY step
            """
        ).fetchall()

    assert len(rows) == 7
    assert [row["step"] for row in rows] == list(range(1, 8))
    assert [row["name"] for row in rows] == [
        "需求完善",
        "系统架构设计",
        "代码审计与重构",
        "人工审计",
        "分阶段写码",
        "调BUG",
        "开发计划生成",
    ]
    assert all(row["is_default"] == 1 for row in rows)
    assert all(row["is_custom"] == 0 for row in rows)
    assert "Senior PM & Business Architect" in rows[0]["content"]
    assert "高级系统架构师" in rows[1]["content"]
    assert "Audit Pillars" in rows[2]["content"]
    assert [rows[index]["content"] for index in (3, 4, 5)] == ["待补充", "待补充", "待补充"]
    assert "{{initial_requirement}}" in rows[6]["content"]
    assert "{{prev_step_output}}" in rows[6]["content"]
