"""
FastAPI Main Application
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
    backup_count=config.LOG_BACKUP_COUNT
)

app = FastAPI(
    title="MoZhi Blog API",
    description="博客后端 API 接口文档",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
    logger.exception(f"服务器内部错误: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "msg": f"服务器内部错误: {str(exc)}",
            "data": None
        }
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
        logger.info("数据库表初始化完成")
    except Exception as exc:
        logger.error(f"数据库连接失败: {exc}")
        logger.warning("请检查数据库配置并确认 MySQL 服务已启动")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=config.API_PORT, reload=True)
