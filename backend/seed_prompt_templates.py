from configparser import RawConfigParser
from pathlib import Path
import sys
from typing import TypedDict

from sqlmodel import Session, select


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.database import create_db_engine
from backend.models import PromptTemplate


SEED_FILE = Path(__file__).resolve().parent / "seed_data" / "prompt_templates.ini"


class PromptTemplateSeed(TypedDict):
    step: int
    name: str
    content: str


def load_prompt_template_seeds() -> list[PromptTemplateSeed]:
    parser = RawConfigParser()
    loaded_files = parser.read(SEED_FILE, encoding="utf-8")
    if loaded_files != [str(SEED_FILE)]:
        raise FileNotFoundError(SEED_FILE)

    seeds: list[PromptTemplateSeed] = []
    for section in parser.sections():
        seeds.append(
            {
                "step": parser.getint(section, "step"),
                "name": parser.get(section, "name").strip(),
                "content": parser.get(section, "content").strip(),
            }
        )
    return sorted(seeds, key=lambda seed: seed["step"])


def seed_prompt_templates() -> None:
    engine = create_db_engine()
    seeds = load_prompt_template_seeds()

    with Session(engine) as session:
        for seed in seeds:
            prompt_template = session.exec(
                select(PromptTemplate).where(
                    PromptTemplate.step == seed["step"],
                    PromptTemplate.is_default == True,
                )
            ).first()

            if prompt_template is None:
                session.add(
                    PromptTemplate(
                        step=seed["step"],
                        name=seed["name"],
                        content=seed["content"],
                    )
                )
                continue

            prompt_template.name = seed["name"]
            prompt_template.content = seed["content"]
            prompt_template.is_default = True
            prompt_template.is_custom = False

        session.commit()


if __name__ == "__main__":
    seed_prompt_templates()
