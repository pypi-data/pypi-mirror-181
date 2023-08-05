"""
Retorna uma lista de generos
"""

# Apps
from kernel_catalogo_videos.core.application.dto import PaginationOutput
from kernel_catalogo_videos.genres.application.use_cases.dto import GenreOutputDTO


class SearchGenreOutput(PaginationOutput[GenreOutputDTO, str]):
    pass
