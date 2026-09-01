from contextlib import asynccontextmanager

from api.db.session import init_db
from api.events import router as event_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup up
    init_db()
    yield
    # clean up


from api.limiter import limiter
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_router, prefix='/api/events')


import os

from fastapi.staticfiles import StaticFiles

public_dir = os.path.join(os.path.dirname(__file__), "public")
app.mount("/static", StaticFiles(directory=public_dir), name="static")

@app.get("/")
def read_root():
    return {"message": "Analytics-api"}


@app.get("/health")
def read_api_health():
    return {"status": "ok"}