"""
Listar videos
"""


# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.dto import PaginationOutputMapper
from kernel_catalogo_videos.core.domain.repositories import SearchParams, SearchResult
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.videos.domain.repositories import VideoRepository
from kernel_catalogo_videos.videos.application.use_cases.dto import VideoOutputDTO, VideoOutputMapper
from kernel_catalogo_videos.videos.application.use_cases.search.input import SearchVideoInput
from kernel_catalogo_videos.videos.application.use_cases.search.output import SearchVideoOutput


class SearchVideosUseCase(UseCase[SearchVideoInput, SearchVideoOutput]):
    """
    Classe para listar videos
    """

    repo: VideoRepository

    def __init__(self, repo: VideoRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: SearchVideoInput) -> SearchVideoOutput:
        if self.logger:
            self.logger.info("search.video.usecase", message="Initial Payload", input_params=asdict(input_params))

        search_params = SearchParams(**asdict(input_params))

        result = self.repo.search(params=search_params)

        if self.logger:
            self.logger.info("search.video.usecase", message="Entities listed")

        return self.__to_output(result=result)

    def __to_output(self, result: SearchResult):
        items = list(
            map(
                lambda video: VideoOutputMapper.to_output(klass=VideoOutputDTO, video=video),
                result.items,
            )
        )
        return PaginationOutputMapper.from_child(SearchVideoOutput).to_output(items=items, result=result)
