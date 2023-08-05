"""
Listar generos
"""


# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.dto import PaginationOutputMapper
from kernel_catalogo_videos.core.domain.repositories import SearchParams, SearchResult
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.genres.domain.repositories import GenreRepository
from kernel_catalogo_videos.genres.application.use_cases.dto import GenreOutputDTO, GenreOutputMapper
from kernel_catalogo_videos.genres.application.use_cases.search.input import SearchGenreInput
from kernel_catalogo_videos.genres.application.use_cases.search.output import SearchGenreOutput


class SearchGenresUseCase(UseCase[SearchGenreInput, SearchGenreOutput]):
    """
    Classe para listar generos
    """

    repo: GenreRepository

    def __init__(self, repo: GenreRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: SearchGenreInput) -> SearchGenreOutput:
        if self.logger:
            self.logger.info("search.genre.usecase", message="Initial Payload", input_params=asdict(input_params))

        search_params = SearchParams(**asdict(input_params))

        result = self.repo.search(params=search_params)

        if self.logger:
            self.logger.info("search.genre.usecase", message="Entities listed")

        return self.__to_output(result=result)

    def __to_output(self, result: SearchResult):
        items = list(
            map(
                lambda genre: GenreOutputMapper.to_output(klass=GenreOutputDTO, genre=genre),
                result.items,
            )
        )
        return PaginationOutputMapper.from_child(SearchGenreOutput).to_output(items=items, result=result)
