"""
Input para atualizar um genero
"""
# Python
from typing import List, Optional
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre


@dataclass(slots=True, frozen=False)
class UpdateGenreInput:
    id: str  # pylint: disable=invalid-name
    categories: List[str]
    title: str
    slug: Optional[str] = Genre.get_field("slug").default
    status: Optional[int] = Genre.get_field("status").default
    is_deleted: Optional[bool] = Genre.get_field("is_deleted").default
