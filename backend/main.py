"""
FastAPI main application.
"""
import pydantic
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import config
from logger import setup_logger
from models import create_tables
from routes import (
    admin_router,
    article_router,
    category_router,
    friendlink_router,
    moment_router,
    rss_router,
    sitemap_router,
    tag_router,
)

pydantic.DATETIME_STRING_FORMATS = [
    "iso8601",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
]

logger = setup_logger(
    log_level=config.LOG_LEVEL,
    log_dir=config.LOG_DIR,
    backup_count=config.LOG_BACKUP_COUNT,
)

app = FastAPI(
    title="MoZhi Blog API",
    description="MoZhi Blog backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled server error - method: %s, path: %s, detail: %s",
        request.method,
        request.url.path,
        str(exc),
    )
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "msg": "服务器内部错误，请稍后重试。",
            "data": None,
        },
    )


app.include_router(admin_router)
app.include_router(article_router)
app.include_router(category_router)
app.include_router(friendlink_router)
app.include_router(moment_router)
app.include_router(tag_router)
app.include_router(rss_router)
app.include_router(sitemap_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "MoZhi Blog API is running"}


@app.on_event("startup")
async def startup_event():
    try:
        create_tables()
        logger.info("Database tables initialized.")
    except Exception as exc:
        logger.error("Database initialization failed: %s", exc)
        logger.warning("Please verify the database configuration and MySQL service status.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=config.API_PORT, reload=True)
