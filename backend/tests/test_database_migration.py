import os
import sqlite3
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALEMBIC_CONFIG = PROJECT_ROOT / "backend" / "alembic.ini"


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


def table_columns(connection: sqlite3.Connection, table_name: str) -> dict[str, sqlite3.Row]:
    return {
        row["name"]: row
        for row in connection.execute(f'PRAGMA table_info("{table_name}")').fetchall()
    }


def test_alembic_upgrade_creates_projects_and_step_outputs(tmp_path: Path) -> None:
    database_path = tmp_path / "app.db"
    database_url = f"sqlite:///{database_path}"
    run_alembic_upgrade(database_url)
    run_alembic_upgrade(database_url)

    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row

        projects = table_columns(connection, "projects")
        step_outputs = table_columns(connection, "step_outputs")
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
    assert versions == ["20260623_0001"]
