"""
Caso de uso para criar um genero
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.genres.domain.repositories import GenreRepository
from kernel_catalogo_videos.genres.application.use_cases.delete.input import DeleteGenreInput


class DeleteGenreUseCase(UseCase[DeleteGenreInput, None]):
    """
    Classe para deletar um genero
    """

    repo: GenreRepository

    def __init__(self, repo: GenreRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: DeleteGenreInput) -> None:
        if self.logger:
            self.logger.info("delete.genre.usecase", message="Initial Payload", input_params=asdict(input_params))

        # pylint: disable=unexpected-keyword-arg
        self.repo.delete(input_params.id)

        if self.logger:
            self.logger.info("delete.genre.usecase", message="Entity deleted")
