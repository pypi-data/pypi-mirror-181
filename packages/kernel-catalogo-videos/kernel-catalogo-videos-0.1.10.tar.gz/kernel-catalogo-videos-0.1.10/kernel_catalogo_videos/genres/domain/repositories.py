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
from .entities import Genre


class _SearchParams(DefaultSearchParams):
    """
    Genres Search Result
    Privadas do modulo
    Sendo utilizadas com o typing da classe e da innerclass
    """

    pass


class _SearchResult(DefaultSearchResult):
    """
    Genres Search Result
    Privadas do modulo
    Sendo utilizadas com o typing da classe e da innerclass
    """

    pass


class GenreRepository(SearchableRepositoryInterface[Genre, _SearchParams, _SearchResult], abc.ABC):
    """
    Classe para tratar um genero
    """

    SearchParams = _SearchParams
    SearchResult = _SearchResult
