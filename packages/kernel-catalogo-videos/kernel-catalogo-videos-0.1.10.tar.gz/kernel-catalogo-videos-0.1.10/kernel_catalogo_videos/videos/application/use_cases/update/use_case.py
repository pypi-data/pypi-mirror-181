"""
Caso de uso para atualizar um video
"""
# pylint: disable=duplicate-code

# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.utils import ACTIVE_STATUS, INACTIVE_STATUS
from kernel_catalogo_videos.videos.domain.entities import Video
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.videos.domain.repositories import VideoRepository
from kernel_catalogo_videos.videos.application.use_cases.dto import VideoOutputMapper
from kernel_catalogo_videos.videos.application.use_cases.update.input import UpdateVideoInput
from kernel_catalogo_videos.videos.application.use_cases.update.output import UpdateVideoOutput


class UpdateVideoUseCase(UseCase[UpdateVideoInput, UpdateVideoOutput]):
    """
    Atualizar um video
    """

    repo: VideoRepository

    def __init__(self, repo: VideoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: UpdateVideoInput) -> UpdateVideoOutput:
        if self.logger:
            self.logger.info("update.video.usecase", message="Initial Payload", input_params=asdict(input_params))

        entity = self.repo.find_by_id(input_params.id)

        if self.logger:
            self.logger.info("update.video.usecase", message="Founded entity", entity=entity.to_dict())

        entity.update(
            data={
                "title": input_params.title,
                "categories": input_params.categories,
                "genres": input_params.genres,
                "slug": input_params.slug,
                "year_launched": input_params.year_launched,
                "opened": input_params.opened,
                "rating": input_params.rating,
                "duration": input_params.duration,
                "is_deleted": input_params.is_deleted,
            }
        )

        if input_params.status == ACTIVE_STATUS:
            entity.activate()

        if input_params.status == INACTIVE_STATUS:
            entity.deactivate()

        if self.logger:
            self.logger.info("update.video.usecase", message="Entity updated", entity=entity.to_dict())

        self.repo.update(entity=entity)
        if self.logger:
            self.logger.info("create.video.usecase", message="Entity saved")

        return self.__to_output(video=entity)

    def __to_output(self, video: Video):
        return VideoOutputMapper.to_output(klass=UpdateVideoOutput, video=video)
