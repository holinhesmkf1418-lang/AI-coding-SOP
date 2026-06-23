from typing import Optional

from sqlalchemy import Engine, event
from sqlmodel import Session, create_engine

from backend.core.config import get_database_url


def is_sqlite_url(database_url: str) -> bool:
    return database_url.startswith("sqlite")


def get_connect_args(database_url: str) -> dict[str, bool]:
    if is_sqlite_url(database_url):
        return {"check_same_thread": False}
    return {}


def enable_sqlite_pragmas(engine: Engine) -> None:
    if not is_sqlite_url(str(engine.url)):
        return

    @event.listens_for(engine, "connect")
    def set_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_db_engine(database_url: Optional[str] = None) -> Engine:
    resolved_database_url = database_url or get_database_url()
    engine = create_engine(
        resolved_database_url,
        connect_args=get_connect_args(resolved_database_url),
    )
    enable_sqlite_pragmas(engine)
    return engine


engine = create_db_engine()


def get_session() -> Session:
    with Session(engine) as session:
        yield session
