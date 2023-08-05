# Python
from typing import List, Generic, TypeVar, Optional
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.core.domain.repositories import SearchResult

Filter = TypeVar("Filter")
Item = TypeVar("Item")


@dataclass(slots=True, frozen=True)
class SearchInput(Generic[Filter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    sort_direction: Optional[str] = None
    filters: Optional[Filter] = None


@dataclass(slots=True, frozen=True)
class PaginationOutput(Generic[Item, Filter]):
    items: List[Item]
    current_page: int
    per_page: int
    last_page: int
    sort: Optional[str]
    sort_direction: Optional[str]
    filters: Optional[Filter]
    total: int


Output = TypeVar("Output", bound=PaginationOutput)


@dataclass(slots=True, frozen=True)
class PaginationOutputMapper:
    output_child: Output

    @staticmethod
    def from_child(output_child: Output):
        return PaginationOutputMapper(output_child)

    def to_output(self, items: List[Item], result: SearchResult) -> PaginationOutput[Item, Filter]:
        return self.output_child(
            items=items,
            current_page=result.current_page,
            per_page=result.per_page,
            last_page=result.last_page,
            sort=result.sort,
            sort_direction=result.sort_direction,
            filters=result.filters,
            total=result.total,
        )
