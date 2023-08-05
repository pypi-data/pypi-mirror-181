"""
Input para atualizar um video
"""
# Python
from typing import List, Optional
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.videos.domain.entities import Video


@dataclass(slots=True, frozen=False)
class UpdateVideoInput:
    id: str  # pylint: disable=invalid-name
    title: str
    categories: List[str]
    genres: List[str]
    slug: Optional[str] = Video.get_field("slug").default
    year_launched: int = Video.get_field("year_launched").default
    opened: bool = Video.get_field("opened").default
    rating: str = Video.get_field("rating").default
    duration: int = Video.get_field("duration").default
    status: Optional[int] = Video.get_field("status").default
    is_deleted: Optional[bool] = Video.get_field("is_deleted").default
