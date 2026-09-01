from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request
from fastapi.security import APIKeyHeader
from sqlalchemy import case, func
from sqlmodel import Session, select
from timescaledb.hyperfunctions import time_bucket

from api.db.config import settings
from api.db.session import engine, get_session
from api.limiter import limiter

api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: Annotated[str, Depends(api_key_header)]):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

from .models import EventBucketSchema, EventCreateSchema, EventModel
from .utils import get_location_from_ip

router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
    "/",
    "/about",
    "/pricing",
    "/contact",
    "/blog",
    "/products",
    "/login",
    "/signup",
    "/dashboard",
    "/settings",
]


@router.get("/", response_model=list[EventBucketSchema])
def read_events(
    session: Annotated[Session, Depends(get_session)],
    api_key: Annotated[str, Depends(get_api_key)],
    duration: Annotated[str, Query()] = "1 day",
    pages: Annotated[list[str] | None, Query()] = None,
):
    os_case = case(
        (EventModel.user_agent.ilike("%windows%"), "Windows"),
        (EventModel.user_agent.ilike("%macintosh%"), "MacOS"),
        (EventModel.user_agent.ilike("%iphone%"), "iOS"),
        (EventModel.user_agent.ilike("%android%"), "Android"),
        (EventModel.user_agent.ilike("%linux%"), "Linux"),
        else_="Other",
    ).label("operating_system")

    bucket = time_bucket(duration, EventModel.time)

    lookup_pages = (
        pages
        if isinstance(pages, list) and len(pages) > 0
        else DEFAULT_LOOKUP_PAGES
    )

    query = (
        select(
            bucket.label("bucket"),
            os_case,
            EventModel.page.label("page"),
            func.avg(EventModel.duration).label("avg_duration"),
            func.count().label("count"),
        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket,
            os_case,
            EventModel.page,
        )
        .order_by(
            bucket,
            os_case,
            EventModel.page,
        )
    )

    results = session.exec(query).all()

    return [
        EventBucketSchema(
            bucket=row.bucket,
            operating_system=row.operating_system,
            page=row.page,
            avg_duration=float(row.avg_duration or 0.0),
            count=row.count,
        )
        for row in results
    ]


def process_and_save_event(data: dict):
    country, city = get_location_from_ip(data.get("ip_address"))
    data["country"] = country
    data["city"] = city
    
    obj = EventModel.model_validate(data)
    with Session(engine) as session:
        session.add(obj)
        session.commit()

@router.post("/", response_model=dict)
@limiter.limit("60/minute")
def create_event(
    payload: EventCreateSchema,
    request: Request,
    background_tasks: BackgroundTasks,
):
    data = payload.model_dump()
    if not data.get("ip_address") and request.client:
        data["ip_address"] = request.client.host

    background_tasks.add_task(process_and_save_event, data)

    return {"status": "processing"}


@router.get("/{event_id}", response_model=EventModel)
def get_event(
    event_id: int,
    session: Annotated[Session, Depends(get_session)],
    api_key: Annotated[str, Depends(get_api_key)],
):
    query = select(EventModel).where(EventModel.id == event_id)

    result = session.exec(query).first()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return result