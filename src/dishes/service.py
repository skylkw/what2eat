from core.exception import AlreadyExistsException, NotFoundException
from dishes.repository import DishRepository
from dishes.schema import DishCreate, DishResponse, DishUpdate


class DishService:
    """业务逻辑层，处理菜品相关的操作"""

    def __init__(self, repository: DishRepository) -> None:
        self.repository = repository

    async def create_dish(self, dish: DishCreate) -> DishResponse:
        """创建新菜品"""
        existing_dish = await self.repository.get_dish_by_name(dish.name)
        if existing_dish:
            raise AlreadyExistsException(
                detail=f"Dish with name '{dish.name}' already exists."
            )
        res = await self.repository.create_dish(dish.model_dump())

        return DishResponse.model_validate(res)

    async def get_dish_by_id(self, dish_id: int) -> DishResponse | None:
        """根据ID获取菜品"""
        res = await self.repository.get_dish_by_id(dish_id)
        if res is None:
            raise NotFoundException(detail=f"Dish with ID '{dish_id}' not found.")
        return DishResponse.model_validate(res)

    async def list_dishes(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[DishResponse]:
        """获取菜品列表"""
        res = await self.repository.get_all_dishes(
            search=search,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )
        return [DishResponse.model_validate(dish) for dish in res]

    async def update_dish(self, dish_id: int, dish: DishUpdate) -> DishResponse:
        """更新菜品"""
        existing_dish = await self.repository.get_dish_by_id(dish_id)
        if not existing_dish:
            raise NotFoundException(f"Dish with id {dish_id} not found")

        # 检查名称是否冲突（仅当提供了新名称时）
        if dish.name is not None and dish.name != existing_dish.name:
            dish_with_same_name = await self.repository.get_dish_by_name(dish.name)
            if dish_with_same_name:
                raise AlreadyExistsException(
                    detail=f"Dish with name '{dish.name}' already exists."
                )

        update_payload = dish.model_dump(exclude_unset=True, exclude_none=True)
        updated_dish = await self.repository.update_dish(dish_id, update_payload)
        return DishResponse.model_validate(updated_dish)

    async def delete_dish(self, dish_id: int) -> None:
        """删除菜品"""
        deleted = await self.repository.delete_dish(dish_id)
        if not deleted:
            raise NotFoundException(f"Dish with id {dish_id} not found")
