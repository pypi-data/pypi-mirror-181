"""
Output retornando os dados de uma categoria
"""
# pylint: disable=duplicate-code

# Python
from typing import List, TypeVar, Optional
from datetime import datetime
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.videos.domain.entities import RATING_EIGHTEEN_YEARS, Video


@dataclass(slots=True, frozen=True)
class VideoOutputDTO:
    id: str  # pylint: disable=invalid-name
    title: str
    slug: str
    categories: List[str]
    genres: List[str]
    is_deleted: bool
    created_at: datetime
    year_launched: int = 2022
    opened: bool = True
    rating: str = RATING_EIGHTEEN_YEARS
    duration: int = 50
    status: Optional[int] = 1
    thumb_file: Optional[str] = ""
    banner_file: Optional[str] = ""
    trailer_file: Optional[str] = ""
    video_file: Optional[str] = ""


Output = TypeVar("Output", bound=VideoOutputDTO)


class VideoOutputMapper:
    @staticmethod
    def to_output(klass: Output, video: Video) -> Output:
        return klass(
            id=video.id,
            title=video.title,
            slug=video.slug,
            year_launched=video.slug,
            opened=video.opened,
            rating=video.rating,
            duration=video.duration,
            thumb_file=video.thumb_file,
            banner_file=video.banner_file,
            trailer_file=video.trailer_file,
            video_file=video.video_file,
            status=video.status,
            is_deleted=video.is_deleted,
            created_at=video.created_at,
        )
