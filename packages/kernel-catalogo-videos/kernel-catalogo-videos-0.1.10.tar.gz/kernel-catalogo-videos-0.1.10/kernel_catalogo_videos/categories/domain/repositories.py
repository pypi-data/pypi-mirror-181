"""
Define os repositories para a categoria
"""
# Python
import abc

# Apps
from kernel_catalogo_videos.core.domain.repositories import SearchParams as DefaultSearchParams
from kernel_catalogo_videos.core.domain.repositories import SearchResult as DefaultSearchResult
from kernel_catalogo_videos.core.domain.repositories import SearchableRepositoryInterface

# Local
from .entities import Category


class _SearchParams(DefaultSearchParams):
    """
    Categories Search Result
    Privadas do modulo
    Sendo utilizadas com o typing da classe e da innerclass
    """

    pass


class _SearchResult(DefaultSearchResult):
    """
    Categories Search Result
    Privadas do modulo
    Sendo utilizadas com o typing da classe e da innerclass
    """

    pass


class CategoryRepository(SearchableRepositoryInterface[Category, _SearchParams, _SearchResult], abc.ABC):
    """
    Classe para tratar uma categoria
    """

    SearchParams = _SearchParams
    SearchResult = _SearchResult
