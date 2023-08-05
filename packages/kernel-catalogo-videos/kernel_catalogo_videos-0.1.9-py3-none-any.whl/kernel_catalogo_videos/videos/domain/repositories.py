"""
Define os repositories para um video
"""
# Python
import abc

# Apps
from kernel_catalogo_videos.core.domain.repositories import SearchParams as DefaultSearchParams
from kernel_catalogo_videos.core.domain.repositories import SearchResult as DefaultSearchResult
from kernel_catalogo_videos.core.domain.repositories import SearchableRepositoryInterface

# Local
from .entities import Video


class _SearchParams(DefaultSearchParams):
    """
    Videos Search Result
    Privadas do modulo
    Sendo utilizadas com o typing da classe e da innerclass
    """

    pass


class _SearchResult(DefaultSearchResult):
    """
    Videos Search Result
    Privadas do modulo
    Sendo utilizadas com o typing da classe e da innerclass
    """

    pass


class VideoRepository(SearchableRepositoryInterface[Video, _SearchParams, _SearchResult], abc.ABC):
    """
    Classe para tratar um video
    """

    SearchParams = _SearchParams
    SearchResult = _SearchResult
