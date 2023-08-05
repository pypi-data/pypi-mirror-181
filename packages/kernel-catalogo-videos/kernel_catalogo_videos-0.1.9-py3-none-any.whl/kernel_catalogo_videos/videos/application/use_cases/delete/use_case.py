"""
Caso de uso para criar um video
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.videos.domain.repositories import VideoRepository
from kernel_catalogo_videos.videos.application.use_cases.delete.input import DeleteVideoInput


class DeleteVideoUseCase(UseCase[DeleteVideoInput, None]):
    """
    Classe para deletar um video
    """

    repo: VideoRepository

    def __init__(self, repo: VideoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: DeleteVideoInput) -> None:
        if self.logger:
            self.logger.info("delete.video.usecase", message="Initial Payload", input_params=asdict(input_params))

        # pylint: disable=unexpected-keyword-arg
        self.repo.delete(input_params.id)

        if self.logger:
            self.logger.info("delete.video.usecase", message="Entity deleted")
