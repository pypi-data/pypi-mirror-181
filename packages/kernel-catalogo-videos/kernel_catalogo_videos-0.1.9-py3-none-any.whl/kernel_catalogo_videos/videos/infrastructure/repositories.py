"""
Define os repositories para generos
"""
# Python
from typing import List, Optional

# Apps
from kernel_catalogo_videos.videos.domain.entities import Video
from kernel_catalogo_videos.core.domain.repositories import Filter, InMemorySearchableRepository
from kernel_catalogo_videos.videos.domain.repositories import VideoRepository


class VideoInMemoryRepository(VideoRepository, InMemorySearchableRepository):
    """
    Classe para tratar um repositorio em memória

    TODO: Refatorar para InMemorySearchableRepository
    """

    sortable_fields: List[str] = ["title", "created_at"]

    def _apply_filter(self, items: List[Video], filters: Optional[Filter]):
        if filters:
            items_filtered = filter(lambda item: filters.lower() in item.title.lower(), items)
            return list(items_filtered)

        return items

    def _apply_sort(self, items: List[Video], sort: Optional[str], sort_direction: Optional[str]) -> List[Video]:
        return (
            super()._apply_sort(items, sort=sort, sort_direction=sort_direction)
            if sort
            else super()._apply_sort(items, sort="created_at", sort_direction="desc")
        )
