"""
Buscar um genero
"""
# pylint: disable=duplicate-code
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.castmembers.domain.entities import CastMember
from kernel_catalogo_videos.castmembers.domain.repositories import CastMemberRepository
from kernel_catalogo_videos.castmembers.application.use_cases.dto import CastMemberOutputMapper
from kernel_catalogo_videos.castmembers.application.use_cases.get.input import GetCastMemberInput
from kernel_catalogo_videos.castmembers.application.use_cases.get.output import GetCastMemberOutput


class GetCastMemberUseCase(UseCase[GetCastMemberInput, GetCastMemberOutput]):
    """
    Classe para criar um membro
    """

    repo: CastMemberRepository

    def __init__(self, repo: CastMemberRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: GetCastMemberInput) -> GetCastMemberOutput:
        if self.logger:
            self.logger.info("get.castmember.usecase", message="Initial Payload", input_params=asdict(input_params))

        castmember = self.repo.find_by_id(input_params.id)

        if self.logger:
            self.logger.info("get.castmember.usecase", message="Entity founded")

        return self.__to_output(castmember=castmember)

    def __to_output(self, castmember: CastMember):
        return CastMemberOutputMapper.to_output(klass=GetCastMemberOutput, castmember=castmember)
