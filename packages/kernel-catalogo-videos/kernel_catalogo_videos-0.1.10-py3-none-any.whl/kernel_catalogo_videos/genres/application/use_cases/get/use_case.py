"""
Buscar um genero
"""
# pylint: disable=duplicate-code
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.genres.domain.repositories import GenreRepository
from kernel_catalogo_videos.genres.application.use_cases.dto import GenreOutputMapper
from kernel_catalogo_videos.genres.application.use_cases.get.input import GetGenreInput
from kernel_catalogo_videos.genres.application.use_cases.get.output import GetGenreOutput


class GetGenreUseCase(UseCase[GetGenreInput, GetGenreOutput]):
    """
    Classe para criar um genero
    """

    repo: GenreRepository

    def __init__(self, repo: GenreRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: GetGenreInput) -> GetGenreOutput:
        if self.logger:
            self.logger.info("get.genre.usecase", message="Initial Payload", input_params=asdict(input_params))

        genre = self.repo.find_by_id(input_params.id)

        if self.logger:
            self.logger.info("get.genre.usecase", message="Entity founded")

        return self.__to_output(genre=genre)

    def __to_output(self, genre: Genre):
        return GenreOutputMapper.to_output(klass=GetGenreOutput, genre=genre)
