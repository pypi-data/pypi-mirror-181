"""
Define os repositories para membros
"""
# Python
from typing import List, Optional

# Apps
from kernel_catalogo_videos.core.domain.repositories import Filter, InMemorySearchableRepository
from kernel_catalogo_videos.castmembers.domain.entities import CastMember
from kernel_catalogo_videos.castmembers.domain.repositories import CastMemberRepository


class CastMemberInMemoryRepository(CastMemberRepository, InMemorySearchableRepository):
    """
    Classe para tratar um repositorio em memória

    TODO: Refatorar para InMemorySearchableRepository
    """

    sortable_fields: List[str] = ["name", "created_at"]

    def _apply_filter(self, items: List[CastMember], filters: Optional[Filter]):
        if filters:
            items_filtered = filter(lambda item: filters.lower() in item.name.lower(), items)
            return list(items_filtered)

        return items

    def _apply_sort(
        self, items: List[CastMember], sort: Optional[str], sort_direction: Optional[str]
    ) -> List[CastMember]:
        return (
            super()._apply_sort(items, sort=sort, sort_direction=sort_direction)
            if sort
            else super()._apply_sort(items, sort="created_at", sort_direction="desc")
        )
