"""
Retorna uma lista de categorias
"""

# Apps
from kernel_catalogo_videos.core.application.dto import PaginationOutput
from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputDTO


class SearchCategoryOutput(PaginationOutput[CategoryOutputDTO, str]):
    pass
