import os


DEFAULT_CORS_ORIGINS = ("http://localhost:5173",)


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
