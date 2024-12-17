import asyncio
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import TemplateNotFound

from .secrets import get_secret
from .constants import IS_DEV, API_PREFIX, APP_NAME
from .logger import logger
from .version import __version__
from .routers import dynamic_media
from .database.sql import create_tables

origins = ["*"]

NOT_AUTHORIZED = "Not Authorized"


async def long_running_process_async():
    get_secret("precious")
    while True:
        logger.info("Long running process")
        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    asyncio.create_task(long_running_process_async())
    yield


app = FastAPI(
    title=APP_NAME,
    lifespan=lifespan,
    docs_url="/docs" if IS_DEV else None,
    redoc_url=None,
    contact={
        "name": "{{cookiecutter.full_name}}",
        "email": "{{cookiecutter.email}}",
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(API_PREFIX)
def read_api_root():
    return {"status": "ok", "version": __version__, "name": APP_NAME}


app.include_router(dynamic_media.router, prefix=API_PREFIX)

TEMPLATES = {}


def lazy_templates_loader():
    if "templates" not in TEMPLATES:
        templates = Jinja2Templates(directory="static")
        TEMPLATES["templates"] = templates
    return TEMPLATES["templates"]


@app.get("/{rest_of_path:path}", include_in_schema=False)
async def catch_all(
    request: Request,
    rest_of_path: str,
):
    if rest_of_path.startswith("latest/meta-data"):
        raise HTTPException(status_code=404, detail="Not found")

    try:
        path = (
            f"{rest_of_path}index.html" if rest_of_path.endswith("/") else rest_of_path
        )
        response = lazy_templates_loader().TemplateResponse(path, {"request": request})
        response.headers["Expires"] = (datetime.now(UTC) + timedelta(hours=1)).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )
        return response
    except TemplateNotFound:
        logger.exception(f"Template not found: index.html when serving {rest_of_path}")
        with open("static/index.html") as f:
            return HTMLResponse(f.read())
