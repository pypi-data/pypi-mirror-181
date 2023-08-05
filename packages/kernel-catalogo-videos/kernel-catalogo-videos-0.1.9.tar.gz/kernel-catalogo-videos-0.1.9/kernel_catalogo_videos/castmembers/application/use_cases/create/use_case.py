"""
Caso de uso para criar um membro
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.castmembers.domain.entities import CastMember
from kernel_catalogo_videos.castmembers.domain.factories import CastMemberFactory
from kernel_catalogo_videos.castmembers.domain.repositories import CastMemberRepository
from kernel_catalogo_videos.castmembers.application.use_cases.dto import CastMemberOutputMapper
from kernel_catalogo_videos.castmembers.application.use_cases.create.input import CreateCastMemberInput
from kernel_catalogo_videos.castmembers.application.use_cases.create.output import CreateCastMemberOutput


class CreateGenreUseCase(UseCase[CreateCastMemberInput, CreateCastMemberOutput]):
    """
    Classe para criar um membro
    """

    repo: CastMemberRepository

    def __init__(self, repo: CastMemberRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def save(self, entity: CastMember):
        self.repo.insert(entity)
        if self.logger:
            self.logger.info("create.castmember.usecase", message="Entity saved")

    def execute(self, input_params: CreateCastMemberInput) -> CreateCastMemberOutput:
        if self.logger:
            self.logger.info("create.castmember.usecase", message="Initial Payload", input_params=asdict(input_params))

        castmember_entity = CastMemberFactory(logger=self.logger).create(
            name=input_params.name, kind=input_params.kind, status=input_params.status
        )

        self.save(castmember_entity)

        return self.__to_output(castmember=castmember_entity)

    def __to_output(self, castmember: CastMember):
        return CastMemberOutputMapper.to_output(klass=CreateCastMemberOutput, castmember=castmember)
