from datetime import datetime, timezone

from sqlmodel import Field, SQLModel
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now


class EventModel(TimescaleModel, table=True):
    page: str = Field(default="", index=True)
    user_agent: str | None = Field(default="", index=True)
    ip_address: str | None = Field(default="", index=True)
    referrer: str | None = Field(default="", index=True)
    session_id: str | None = Field(default=None, index=True)
    duration: int | None = Field(default=0)
    country: str | None = Field(default="", index=True)
    city: str | None = Field(default="")

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"


class EventCreateSchema(SQLModel):
    page: str = Field(default="")
    user_agent: str | None = Field(default="", index=True)
    ip_address: str | None = Field(default="", index=True)
    referrer: str | None = Field(default="", index=True)
    session_id: str | None = Field(default=None, index=True)
    duration: int | None = Field(default=0)
    country: str | None = Field(default="", index=True)
    city: str | None = Field(default="")


class EventListSchema(SQLModel):
    results: list[EventModel]
    count: int


class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    ua: str | None = ""
    operating_system: str | None = ""
    avg_duration: float | None = 0.0
    count: int
