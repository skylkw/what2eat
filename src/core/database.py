from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.base_model import Base
from core.config import settings


# 创建数据库引擎和会话工厂
engine = create_async_engine(settings.database_url, **settings.engine_options)
SessionFactory = async_sessionmaker(
    class_=AsyncSession, bind=engine, expire_on_commit=False, autoflush=False
)


# 数据库依赖注入
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session


# 用于临时测试的数据库初始化函数
async def create_db_and_tables():
    async with engine.begin() as conn:
        logger.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created.")
