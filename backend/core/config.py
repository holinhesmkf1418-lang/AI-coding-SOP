import os
from pathlib import Path


DEFAULT_CORS_ORIGINS = ("http://localhost:5173",)
BACKEND_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_PATH = BACKEND_ROOT / "data" / "app.db"


def get_cors_origins() -> list[str]:
    raw_origins = os.getenv("BACKEND_CORS_ORIGINS")
    if raw_origins is None:
        return list(DEFAULT_CORS_ORIGINS)

    configured_origins = [
        origin.strip()
        for origin in raw_origins.split(",")
        if origin.strip()
    ]
    return configured_origins or list(DEFAULT_CORS_ORIGINS)


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DATABASE_PATH}")
