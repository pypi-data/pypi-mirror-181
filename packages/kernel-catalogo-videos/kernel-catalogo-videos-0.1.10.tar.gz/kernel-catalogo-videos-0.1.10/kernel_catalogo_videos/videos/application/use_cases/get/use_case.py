"""
Buscar um video
"""
# pylint: disable=duplicate-code
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.videos.domain.entities import Video
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.videos.domain.repositories import VideoRepository
from kernel_catalogo_videos.videos.application.use_cases.dto import VideoOutputMapper
from kernel_catalogo_videos.videos.application.use_cases.get.input import GetVideoInput
from kernel_catalogo_videos.videos.application.use_cases.get.output import GetVideoOutput


class GetVideoUseCase(UseCase[GetVideoInput, GetVideoOutput]):
    """
    Classe para criar um video
    """

    repo: VideoRepository

    def __init__(self, repo: VideoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: GetVideoInput) -> GetVideoOutput:
        if self.logger:
            self.logger.info("get.video.usecase", message="Initial Payload", input_params=asdict(input_params))

        video = self.repo.find_by_id(input_params.id)

        if self.logger:
            self.logger.info("get.video.usecase", message="Entity founded")

        return self.__to_output(video=video)

    def __to_output(self, video: Video):
        return VideoOutputMapper.to_output(klass=GetVideoOutput, video=video)
