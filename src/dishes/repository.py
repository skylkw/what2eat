from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from dishes.model import Dish

ALLOWED_SORT = {"id", "name", "created_at", "updated_at"}


class RepositoryError(Exception):
    """仓库层异常，封装底层数据库错误"""

    pass


class DishRepository:
    """菜品仓库类，负责与数据库交互以管理菜品数据"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_dish(self, dish_data: dict[str, Any]) -> Dish:
        dish = Dish(**dish_data)
        self.session.add(dish)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(dish)
        return dish

    async def get_dish_by_id(self, dish_id: int) -> Dish | None:
        """根据ID获取菜品"""
        try:
            result = await self.session.get(Dish, dish_id)
            return result
        except SQLAlchemyError as e:
            raise RepositoryError("数据库操作失败") from e

    async def get_dish_by_name(self, name: str) -> Dish | None:
        """根据名称获取菜品"""
        try:
            query = select(Dish).where(Dish.name == name)
            result = await self.session.scalars(query)
            return result.first()
        except SQLAlchemyError as e:
            raise RepositoryError("数据库操作失败") from e

    async def get_all_dishes(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[Dish]:
        """获取所有菜品"""
        try:
            query = select(Dish)
            if search:
                query = query.where(Dish.name.ilike(f"%{search}%"))
            # validate order_by
            if order_by not in ALLOWED_SORT:
                raise RepositoryError(f"不支持的排序字段: {order_by}")
            column = getattr(Dish, order_by)
            if direction.lower() == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
            # validate limit/offset
            limit = max(1, min(limit, 100))
            offset = max(0, offset)
            query = query.limit(limit).offset(offset)
            result = await self.session.scalars(query)
            return list(result)
        except SQLAlchemyError as e:
            raise RepositoryError("数据库查询失败") from e

    async def update_dish(
        self, dish_id: int, update_data: dict[str, Any]
    ) -> Dish | None:
        """更新菜品"""
        try:
            dish = await self.session.get(Dish, dish_id)
            if dish is None:
                return None
            for key, value in update_data.items():
                if hasattr(dish, key):
                    setattr(dish, key, value)
            await self.session.commit()
            await self.session.refresh(dish)
            return dish
        except IntegrityError as e:
            raise RepositoryError("数据完整性错误") from e
        except SQLAlchemyError as e:
            raise RepositoryError("数据库操作失败") from e

    async def delete_dish(self, dish_id: int) -> bool:
        """删除菜品"""
        try:
            dish = await self.session.get(Dish, dish_id)
            if dish is None:
                return False
            await self.session.delete(dish)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            raise RepositoryError("数据库操作失败") from e
