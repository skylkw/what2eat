from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from loguru import logger

from core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # 在应用启动时执行的代码
    logger.info("应用启动中...")
    # await create_db_and_tables()
    yield
    # 在应用关闭时执行的代码
    logger.info("应用关闭中...")
