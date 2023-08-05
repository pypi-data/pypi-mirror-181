"""
Caso de uso para criar um membro
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.castmembers.domain.repositories import CastMemberRepository
from kernel_catalogo_videos.castmembers.application.use_cases.delete.input import DeleteCastMemberInput


class DeleteCastMemberUseCase(UseCase[DeleteCastMemberInput, None]):
    """
    Classe para deletar um membro
    """

    repo: CastMemberRepository

    def __init__(self, repo: CastMemberRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: DeleteCastMemberInput) -> None:
        if self.logger:
            self.logger.info("delete.castmember.usecase", message="Initial Payload", input_params=asdict(input_params))

        # pylint: disable=unexpected-keyword-arg
        self.repo.delete(input_params.id)

        if self.logger:
            self.logger.info("delete.castmember.usecase", message="Entity deleted")
