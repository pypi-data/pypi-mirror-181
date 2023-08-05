"""
Input para retornar uma categoria
"""

# Python
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputDTO


@dataclass(slots=True, frozen=True)
class UpdateCategoryOutput(CategoryOutputDTO):
    pass
