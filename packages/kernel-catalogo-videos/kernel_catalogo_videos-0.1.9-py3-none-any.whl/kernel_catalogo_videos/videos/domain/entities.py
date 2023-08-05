"""
Define uma entidade
"""
# pylint: disable=duplicate-code


# Python
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import field, dataclass

# Third
from slugify import slugify

# Apps
from kernel_catalogo_videos.core.utils import ACTIVE_STATUS, INACTIVE_STATUS, now
from kernel_catalogo_videos.core.domain.entities import Entity

RATING_FREE = "F"
RATING_TEN_YEARS = "10"
RATING_TWELVE_YEARS = "12"
RATING_FOURTEEN_YEARS = "14"
RATING_SIXTEEN_YEAR = "16"
RATING_EIGHTEEN_YEARS = "18"
THUMB_FILE_MAX_SIZE = 1024 * 5
BANNER_FILE_MAX_SIZE = 1024 * 10
TRAILER_FILE_MAX_SIZE = 1024 * 1024 * 1
VIDEO_FILE_MAX_SIZE = 1024 * 1024 * 50  # 50GB


@dataclass(kw_only=True, frozen=True, slots=True)
class Video(Entity):
    """
    Representa os dados da entidade video
    """

    title: str
    slug: str
    categories: List[str]
    genres: List[str]
    year_launched: int = 2022
    opened: bool = True
    rating: str = RATING_EIGHTEEN_YEARS
    duration: int = 50
    status: Optional[int] = ACTIVE_STATUS
    is_deleted: bool = False
    thumb_file: Optional[str] = ""
    banner_file: Optional[str] = ""
    trailer_file: Optional[str] = ""
    video_file: Optional[str] = ""
    created_at: Optional[datetime] = field(default_factory=now)

    def __post_init__(self):
        self.normalize()

    def update(self, data: Dict[str, Any]):
        """
        Atualiza os dados internos da entidade
        """
        for field_name, value in data.items():
            self._set(field_name, value)

        self.normalize()

    def normalize(self):
        slugged = slugify(self.title)
        self._set("slug", slugged)

    def activate(self):
        """
        Seta o atributo status como ativo
        """
        self._set("status", ACTIVE_STATUS)

    def deactivate(self):
        """
        Seta o atributo status como inativo
        """
        self._set("status", INACTIVE_STATUS)
