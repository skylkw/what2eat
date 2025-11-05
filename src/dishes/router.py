from typing import Literal
from fastapi import APIRouter, Path, Query, status
from fastapi import Depends
from loguru import logger

from core.database import get_db

from dishes.repository import DishRepository
from dishes.schema import DishCreate, DishResponse, DishUpdate
from dishes.service import DishService

router = APIRouter(prefix="/dishes", tags=["Dishes"])


async def get_repo(session=Depends(get_db)) -> DishRepository:
    return DishRepository(session)


async def get_dish_service(repo: DishRepository = Depends(get_repo)) -> DishService:
    return DishService(repo)


@router.post("/", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(
    dish: DishCreate,
    service: DishService = Depends(get_dish_service),
):
    """创建新菜品"""
    new_dish = await service.create_dish(dish)
    return new_dish


@router.get("/{dish_id}", response_model=DishResponse)
async def get_dish(
    dish_id: int,
    service: DishService = Depends(get_dish_service),
):
    """根据ID获取菜品"""
    try:
        logger.debug(f"正在获取菜品 ID: {dish_id}")
        dish = await service.get_dish_by_id(dish_id)
        return dish
    except Exception as e:
        logger.error(f"获取 ID 为 {dish_id} 的菜品时出错: {str(e)}")
        raise


@router.get("/", response_model=list[DishResponse])
async def list_dishes(
    search: str | None = Query(None, description="搜索关键词"),
    order_by: Literal["id", "name", "created_at"] = Query("id", description="排序字段"),
    direction: Literal["asc", "desc"] = Query("asc", description="排序方向"),
    limit: int = Query(10, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: DishService = Depends(get_dish_service),
):
    """查询所有菜品"""
    dishes = await service.list_dishes(
        search=search,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset,
    )
    return dishes


@router.patch("/{dish_id}", response_model=DishResponse)
async def update_dish(
    dish: DishUpdate,
    dish_id: int = Path(..., description="菜品ID"),
    service: DishService = Depends(get_dish_service),
):
    """更新菜品"""
    updated_dish = await service.update_dish(dish_id, dish)
    return updated_dish


@router.delete(
    "/{dish_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_dish(
    dish_id: int = Path(..., description="菜品ID"),
    service: DishService = Depends(get_dish_service),
):
    """删除菜品"""

    await service.delete_dish(dish_id)
