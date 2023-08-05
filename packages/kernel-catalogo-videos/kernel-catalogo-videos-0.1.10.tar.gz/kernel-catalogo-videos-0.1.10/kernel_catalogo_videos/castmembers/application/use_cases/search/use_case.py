"""
Listar membros
"""


# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.dto import PaginationOutputMapper
from kernel_catalogo_videos.core.domain.repositories import SearchParams, SearchResult
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.castmembers.domain.repositories import CastMemberRepository
from kernel_catalogo_videos.castmembers.application.use_cases.dto import CastMemberOutputDTO, CastMemberOutputMapper
from kernel_catalogo_videos.castmembers.application.use_cases.search.input import SearchCastMemberInput
from kernel_catalogo_videos.castmembers.application.use_cases.search.output import SearchCastMemberOutput


class SearchCastMembersUseCase(UseCase[SearchCastMemberInput, SearchCastMemberOutput]):
    """
    Classe para listar membros
    """

    repo: CastMemberRepository

    def __init__(self, repo: CastMemberRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: SearchCastMemberInput) -> SearchCastMemberOutput:
        if self.logger:
            self.logger.info("search.castmember.usecase", message="Initial Payload", input_params=asdict(input_params))

        search_params = SearchParams(**asdict(input_params))

        result = self.repo.search(params=search_params)

        if self.logger:
            self.logger.info("search.castmember.usecase", message="Entities listed")

        return self.__to_output(result=result)

    def __to_output(self, result: SearchResult):
        items = list(
            map(
                lambda castmember: CastMemberOutputMapper.to_output(klass=CastMemberOutputDTO, castmember=castmember),
                result.items,
            )
        )
        return PaginationOutputMapper.from_child(SearchCastMemberOutput).to_output(items=items, result=result)
