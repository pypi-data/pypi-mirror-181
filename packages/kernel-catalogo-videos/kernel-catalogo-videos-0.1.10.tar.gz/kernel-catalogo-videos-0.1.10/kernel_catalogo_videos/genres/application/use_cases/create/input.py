"""
Input para criar um genero
"""
# Python
from typing import List, Optional
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre


@dataclass(slots=True, frozen=True)
class CreateGenreInput:
    title: str
    categories: List[str]
    status: Optional[int] = Genre.get_field("status").default
