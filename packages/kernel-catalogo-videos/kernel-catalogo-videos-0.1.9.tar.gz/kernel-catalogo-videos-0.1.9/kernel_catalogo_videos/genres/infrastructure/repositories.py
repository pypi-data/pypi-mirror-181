"""
Define os repositories para generos
"""
# Python
from typing import List, Optional

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre
from kernel_catalogo_videos.core.domain.repositories import Filter, InMemorySearchableRepository
from kernel_catalogo_videos.genres.domain.repositories import GenreRepository


class GenreInMemoryRepository(GenreRepository, InMemorySearchableRepository):
    """
    Classe para tratar um repositorio em memória

    TODO: Refatorar para InMemorySearchableRepository
    """

    sortable_fields: List[str] = ["title", "created_at"]

    def _apply_filter(self, items: List[Genre], filters: Optional[Filter]):
        if filters:
            items_filtered = filter(lambda item: filters.lower() in item.title.lower(), items)
            return list(items_filtered)

        return items

    def _apply_sort(self, items: List[Genre], sort: Optional[str], sort_direction: Optional[str]) -> List[Genre]:
        return (
            super()._apply_sort(items, sort=sort, sort_direction=sort_direction)
            if sort
            else super()._apply_sort(items, sort="created_at", sort_direction="desc")
        )
