"""
Caso de uso para atualizar um membro
"""
# pylint: disable=duplicate-code

# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.utils import ACTIVE_STATUS, INACTIVE_STATUS
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.castmembers.domain.entities import CastMember
from kernel_catalogo_videos.castmembers.domain.repositories import CastMemberRepository
from kernel_catalogo_videos.castmembers.application.use_cases.dto import CastMemberOutputMapper
from kernel_catalogo_videos.castmembers.application.use_cases.update.input import UpdateCastMemberInput
from kernel_catalogo_videos.castmembers.application.use_cases.update.output import UpdateCastMemberOutput


class UpdateCastMemberUseCase(UseCase[UpdateCastMemberInput, UpdateCastMemberOutput]):
    """
    Atualizar um membro
    """

    repo: CastMemberRepository

    def __init__(self, repo: CastMemberRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: UpdateCastMemberInput) -> UpdateCastMemberOutput:
        if self.logger:
            self.logger.info("update.castmember.usecase", message="Initial Payload", input_params=asdict(input_params))

        entity = self.repo.find_by_id(input_params.id)

        if self.logger:
            self.logger.info("update.castmember.usecase", message="Founded entity", entity=entity.to_dict())

        entity.update(data={"title": input_params.title})

        if input_params.status == ACTIVE_STATUS:
            entity.activate()

        if input_params.status == INACTIVE_STATUS:
            entity.deactivate()

        if self.logger:
            self.logger.info("update.castmember.usecase", message="Entity updated", entity=entity.to_dict())

        self.repo.update(entity=entity)
        if self.logger:
            self.logger.info("create.castmember.usecase", message="Entity saved")

        return self.__to_output(castmember=entity)

    def __to_output(self, castmember: CastMember):
        return CastMemberOutputMapper.to_output(klass=UpdateCastMemberOutput, castmember=castmember)
