from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


# 公共字段基类
class DishBase(BaseModel):
    name: Annotated[str, Field(..., title="菜品名称", max_length=255)]
    description: Annotated[str | None, Field(None, title="菜品描述", max_length=500)]


# 创建模型
class DishCreate(DishBase):
    pass


# 更新模型
class DishUpdate(BaseModel):
    name: Annotated[str | None, Field(None, title="菜品名称", max_length=255)]
    description: Annotated[str | None, Field(None, title="菜品描述", max_length=500)]


# 响应模型（含时间戳）
class DishResponse(DishBase):
    id: Annotated[int, Field(..., title="菜品ID")]
    created_at: Annotated[datetime, Field(..., title="创建时间")]
    updated_at: Annotated[datetime, Field(..., title="更新时间")]

    model_config = ConfigDict(from_attributes=True)


# 查询参数模型
class DishQueryParams(BaseModel):
    """菜品列表查询参数"""

    search: Annotated[
        str | None, Field(description="搜索关键词，可根据名称或描述进行模糊匹配")
    ] = None

    order_by: Annotated[
        Literal["id", "name", "created_at"],
        Field(description="排序字段，可选：id、name、created_at"),
    ] = "id"

    direction: Annotated[
        Literal["asc", "desc"],
        Field(description="排序方向，可选：asc（升序）、desc（降序）"),
    ] = "asc"

    limit: Annotated[
        int, Field(ge=1, le=500, description="每页返回的最大条数（1-500）")
    ] = 10

    offset: Annotated[int, Field(ge=0, description="查询偏移量，用于分页")] = 0
