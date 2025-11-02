from functools import lru_cache
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    app_name: str = "What to Eat"
    debug: bool = False
    # 数据库类型
    db_type: Literal["sqlite", "mysql", "postgresql"] = "sqlite"

    # PostgreSQL 配置
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_user: str = "user"
    pg_password: str = "password"
    pg_name: str = "what2eat"

    # MySQL 配置
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "user"
    mysql_password: str = "password"
    mysql_name: str = "what2eat"

    # SQLite 配置
    sqlite_db_path: str = "data/what2eat.db"

    # 连接池配置（适用于 MySQL 和 PostgreSQL）
    # 中等配置，适合大多数应用场景
    pool_size: int = 20  # 连接池大小 低：-，高：+
    max_overflow: int = 10  # 连接池最大溢出，低：-，高：+
    pool_timeout: int = 30  # 连接池超时时间（秒），低：+，高：-
    pool_pre_ping: bool = True  # 取连接时检查连接是否可用，低：False，高：True
    # 可选调优参数
    pool_recycle: int = 3600  # 连接池中连接的最大生命周期（秒），低：-，高：+
    pool_use_lifo: bool = False  # 是否使用 LIFO 策略获取连接，低：False，高：True
    echo_sql: bool = (
        False  # 是否输出 SQL 语句日志，开发环境可设为 True，生产环境设为 False
    )

    @computed_field
    @property
    def database_url(self) -> str:
        """根据配置生成数据库连接 URL"""
        if self.db_type == "postgresql":
            return (
                f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}"
                f"@{self.pg_host}:{self.pg_port}/{self.pg_name}"
            )
        elif self.db_type == "mysql":
            return (
                f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}"
                f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_name}"
            )
        elif self.db_type == "sqlite":  # 默认使用 SQLite
            return f"sqlite+aiosqlite:///{self.sqlite_db_path}"
        else:
            raise ValueError(f"Unsupported db_type: {self.db_type}")

    @computed_field
    @property
    def engine_options(self) -> dict:
        """根据连接池配置生成引擎选项字典"""
        options = {}
        if self.db_type in {"postgresql", "mysql"}:
            options = {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "pool_timeout": self.pool_timeout,
                "pool_pre_ping": self.pool_pre_ping,
                "pool_recycle": self.pool_recycle,
                "pool_use_lifo": self.pool_use_lifo,
                "echo": self.echo_sql,
            }
        elif self.db_type == "sqlite":
            options = {
                "echo": self.echo_sql,
            }
        return options

    # JWT 配置
    jwt_secret_key: str = "your_secret_key"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


@lru_cache
def get_settings() -> Settings:
    """获取应用配置实例"""
    return Settings()


settings = get_settings()
