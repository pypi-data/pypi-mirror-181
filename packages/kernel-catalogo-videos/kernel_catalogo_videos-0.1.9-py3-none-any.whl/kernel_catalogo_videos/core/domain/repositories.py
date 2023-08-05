"""
Modulo seedwork para repositories classes
"""

# Python
import abc
import math
from typing import Any, List, Generic, TypeVar, Optional
from dataclasses import Field, field, dataclass

# Apps
from kernel_catalogo_videos.core.domain.entities import Entity
from kernel_catalogo_videos.core.domain.exceptions import NotFoundException
from kernel_catalogo_videos.core.domain.unique_entity_id import UniqueEntityId

ET = TypeVar("ET", bound=Entity)
Input = TypeVar("Input")
Output = TypeVar("Output")
Filter = TypeVar("Filter", str, Any)


class RepositoryInterface(Generic[ET], abc.ABC):
    """
    Interface para definir o contrato dos metodos
    """

    @abc.abstractmethod
    def insert(self, entity: ET) -> None:
        """
        Inserir uma entidade
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        """
        Procurar uma entidade por id
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all(self) -> List[ET]:
        """
        Buscar todas as entidades
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update(self, entity: ET) -> None:
        """
        Atualizar uma entidade
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, entity_id: str | UniqueEntityId) -> None:
        """
        Deletar uma entidade por id
        """
        raise NotImplementedError()


class SearchableRepositoryInterface(Generic[ET, Input, Output], RepositoryInterface[ET], abc.ABC):
    """
    Contrato para implementar uma busca
    """

    sortable_fields: List[str] = []

    @abc.abstractmethod
    def search(self, params: Input) -> Output:
        """
        Buscar um item de acordo com os parametros
        """
        raise NotImplementedError()


@dataclass(slots=True, kw_only=True)
class SearchParams(Generic[Filter]):
    """
    Definição de parametros de busca genérico
    """

    page: Optional[int] = 1
    per_page: Optional[int] = 10
    sort: Optional[str] = None
    sort_direction: Optional[str] = None
    filters: Optional[Filter] = None

    def __post_init__(self):
        self._normalize_page()
        self._normalize_per_page()
        self._normalize_sort()
        self._normalize_sort_direction()
        self._normalize_filters()

    def _normalize_page(self):
        page = self._convert_to_int(self.page)
        if page <= 0:
            page = self._get_dataclass_field("page").default

        self.page = page

    def _normalize_per_page(self):
        per_page = self._convert_to_int(self.per_page, default=10)

        if per_page <= 0:
            per_page = self._get_dataclass_field("per_page").default

        self.per_page = per_page

    def _normalize_sort(self):
        self.sort = None if self.sort == "" or self.sort is None else str(self.sort)

    def _normalize_sort_direction(self):
        if not self.sort:
            self.sort_direction = None

        sort_direction = str(self.sort_direction).lower()

        self.sort_direction = "asc" if sort_direction not in ["asc", "desc"] else sort_direction

    def _normalize_filters(self):
        self.filters = None if self.filters == "" or self.filters is None else str(self.filters)

    def _convert_to_int(self, value: Any, default=1) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _get_dataclass_field(self, field_name):
        # pylint: disable=no-member
        return SearchParams.__dataclass_fields__[field_name]

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        # pylint: disable=no-member
        return cls.__dataclass_fields__[entity_field]


@dataclass(slots=True, kw_only=True, frozen=True)
class SearchResult(Generic[ET, Filter]):
    """
    Definição resultados de uma busca genérico
    """

    items: List[ET]
    current_page: int
    per_page: int
    last_page: int = field(init=False)
    sort: Optional[str] = None
    sort_direction: Optional[str] = None
    filters: Optional[Filter] = None
    total: int = 0

    def __post_init__(self):
        object.__setattr__(self, "last_page", math.ceil(self.total / self.per_page))

    def to_dict(self):
        """
        Retorna um dicionario com os dados instanciados
        """
        return {
            "items": self.items,
            "total": self.total,
            "current_page": self.current_page,
            "per_page": self.per_page,
            "last_page": self.last_page,
            "sort": self.sort,
            "sort_direction": self.sort_direction,
            "filters": self.filters,
        }


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[ET], abc.ABC):
    """
    Repositorio com as principais operações CRUD em memória
    """

    items: List[ET] = field(default_factory=lambda: [])

    def insert(self, entity: ET) -> None:
        self.items.append(entity)

    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        entity_id_str = str(entity_id)

        return self._get(entity_id_str)

    def find_all(self) -> List[ET]:
        return self.items

    def update(self, entity: ET) -> None:

        entity_founded = self._get(entity.id)
        index = self.items.index(entity_founded)
        self.items[index] = entity

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        entity_id_str = str(entity_id)
        entity_founded = self._get(entity_id_str)
        self.items.remove(entity_founded)

    def _get(self, entity_id: str):
        entity = next(filter(lambda item: item.id == entity_id, self.items), None)

        if entity is None:
            raise NotFoundException(f"Entity not found using ID '{entity_id}'")

        return entity


class InMemorySearchableRepository(
    Generic[ET, Filter],
    InMemoryRepository[ET],
    SearchableRepositoryInterface[ET, SearchParams[Filter], SearchResult[ET, Filter]],
    abc.ABC,
):
    """
    Repositório que herda as principais operacoes de CRUD mais o SEARCH
    """

    def search(self, params: SearchParams[Filter]) -> SearchResult[ET, Filter]:
        items_filtered = self._apply_filter(self.items, params.filters)
        items_sorted = self._apply_sort(items_filtered, params.sort, params.sort_direction)
        items_paginated = self._apply_paginate(items_sorted, params.page, params.per_page)

        return SearchResult(
            items=items_paginated,
            total=len(items_filtered),
            current_page=params.page,
            per_page=params.per_page,
            sort=params.sort,
            sort_direction=params.sort_direction,
            filters=params.filters,
        )

    @abc.abstractmethod
    def _apply_filter(self, items: List[ET], filters: Optional[Filter]):
        raise NotImplementedError()

    def _apply_sort(self, items: List[ET], sort: Optional[str], sort_direction: Optional[str]) -> List[ET]:
        if sort and sort in self.sortable_fields:
            is_reverse = sort_direction == "desc"
            return sorted(items, key=lambda item: getattr(item, sort), reverse=is_reverse)

        return items

    def _apply_paginate(self, items: List[ET], page: int, per_page: int) -> List[ET]:
        start = (page - 1) * per_page
        limit = start + per_page
        return items[slice(start, limit)]
