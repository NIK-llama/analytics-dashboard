import timescaledb
from sqlmodel import Session, SQLModel

from .config import settings

if settings.database_url == "":
    raise NotImplementedError("DATABASE_URL needs to be set")

engine = timescaledb.create_engine(settings.database_url, settings.db_timezone)

def init_db():
    print("database initialized (migrations handled by alembic)")
    print("creating hypertables")
    timescaledb.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


