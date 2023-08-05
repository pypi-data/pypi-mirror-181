"""
Input para criar uma categoria
"""
# Python
from typing import Optional
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.categories.domain.entities import Category


@dataclass(slots=True, frozen=True)
class CreateCategoryInput:
    title: str
    description: Optional[str] = Category.get_field("description").default
    status: Optional[int] = Category.get_field("status").default
