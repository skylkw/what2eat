from datetime import datetime, timezone

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import settings

database_naming_convention = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    """基础模型类，所有 ORM 模型均继承自此类"""

    metadata = MetaData(naming_convention=database_naming_convention)


class DateTimeMixin:
    """包含创建和更新时间戳的混入类"""

    if settings.db_type in {"postgres", "mysql"}:
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            server_default=func.now(),
            nullable=False,
            index=True,
            comment="创建时间",
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=func.now(),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
            comment="更新时间",
        )
    else:
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            nullable=False,
            index=True,
            comment="创建时间",
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            onupdate=datetime.now(timezone.utc),
            nullable=False,
            comment="更新时间",
        )
