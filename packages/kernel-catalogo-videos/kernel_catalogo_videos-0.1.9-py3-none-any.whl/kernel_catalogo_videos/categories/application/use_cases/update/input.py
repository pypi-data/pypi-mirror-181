"""
Input para atualizar uma categoria
"""
# Python
from typing import Optional
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.categories.domain.entities import Category


@dataclass(slots=True, frozen=False)
class UpdateCategoryInput:
    id: str  # pylint: disable=invalid-name
    title: str
    slug: Optional[str] = Category.get_field("slug").default
    description: Optional[str] = Category.get_field("description").default
    status: Optional[int] = Category.get_field("status").default
    is_deleted: Optional[bool] = Category.get_field("is_deleted").default
