"""
Caso de uso para criar uma categoria
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.videos.domain.entities import Video
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.videos.domain.repositories import VideoRepository
from kernel_catalogo_videos.videos.application.use_cases.dto import VideoOutputMapper
from kernel_catalogo_videos.videos.application.use_cases.create.input import CreateVideoInput
from kernel_catalogo_videos.videos.application.use_cases.create.output import CreateVideoOutput


class CreateVideoUseCase(UseCase[CreateVideoInput, CreateVideoOutput]):
    """
    Classe para criar um video
    """

    repo: VideoRepository

    def __init__(self, repo: VideoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: CreateVideoInput) -> CreateVideoOutput:
        if self.logger:
            self.logger.info("create.video.usecase", message="Initial Payload", input_params=asdict(input_params))

        video = Video(
            title=input_params.title,
            categories=input_params.categories,
            genres=input_params.genres,
            slug=input_params.slug,
            year_launched=input_params.year_launched,
            opened=input_params.opened,
            rating=input_params.rating,
            duration=input_params.duration,
            is_deleted=input_params.is_deleted,
            status=input_params.status,
        )
        video.normalize()

        if self.logger:
            self.logger.info("create.video.usecase", message="Entity created", video=video.to_dict())

        self.repo.insert(video)
        if self.logger:
            self.logger.info("create.video.usecase", message="Entity saved")

        return self.__to_output(video=video)

    def __to_output(self, video: Video):
        return VideoOutputMapper.to_output(klass=CreateVideoOutput, video=video)
