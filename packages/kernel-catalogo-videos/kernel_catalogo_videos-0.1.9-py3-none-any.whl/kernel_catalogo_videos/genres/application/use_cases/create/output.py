"""
Input para retornar um genero
"""

# Python
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.genres.application.use_cases.dto import GenreOutputDTO


@dataclass(slots=True, frozen=True)
class CreateGenreOutput(GenreOutputDTO):
    pass
