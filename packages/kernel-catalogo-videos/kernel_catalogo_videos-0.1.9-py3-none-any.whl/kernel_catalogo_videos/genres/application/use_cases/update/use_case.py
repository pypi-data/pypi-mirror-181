"""
Caso de uso para atualizar um genero
"""
# pylint: disable=duplicate-code

# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.utils import ACTIVE_STATUS, INACTIVE_STATUS
from kernel_catalogo_videos.genres.domain.entities import Genre
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.genres.domain.repositories import GenreRepository
from kernel_catalogo_videos.genres.application.use_cases.dto import GenreOutputMapper
from kernel_catalogo_videos.genres.application.use_cases.update.input import UpdateGenreInput
from kernel_catalogo_videos.genres.application.use_cases.update.output import UpdateGenreOutput


class UpdateGenreUseCase(UseCase[UpdateGenreInput, UpdateGenreOutput]):
    """
    Atualizar um genero
    """

    repo: GenreRepository

    def __init__(self, repo: GenreRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: UpdateGenreInput) -> UpdateGenreOutput:
        if self.logger:
            self.logger.info("update.genre.usecase", message="Initial Payload", input_params=asdict(input_params))

        entity = self.repo.find_by_id(input_params.id)

        if self.logger:
            self.logger.info("update.genre.usecase", message="Founded entity", entity=entity.to_dict())

        entity.update(data={"title": input_params.title})

        if input_params.status == ACTIVE_STATUS:
            entity.activate()

        if input_params.status == INACTIVE_STATUS:
            entity.deactivate()

        if self.logger:
            self.logger.info("update.genre.usecase", message="Entity updated", entity=entity.to_dict())

        self.repo.update(entity=entity)
        if self.logger:
            self.logger.info("create.genre.usecase", message="Entity saved")

        return self.__to_output(genre=entity)

    def __to_output(self, genre: Genre):
        return GenreOutputMapper.to_output(klass=UpdateGenreOutput, genre=genre)
