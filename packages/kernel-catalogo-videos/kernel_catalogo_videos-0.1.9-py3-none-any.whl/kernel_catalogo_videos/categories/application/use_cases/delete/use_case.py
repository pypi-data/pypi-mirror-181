"""
Caso de uso para criar uma categoria
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository
from kernel_catalogo_videos.categories.application.use_cases.delete.input import DeleteCategoryInput


class DeleteCategoryUseCase(UseCase[DeleteCategoryInput, None]):
    """
    Classe para deletar uma categoria
    """

    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: DeleteCategoryInput) -> None:
        if self.logger:
            self.logger.info("delete.category.usecase", message="Initial Payload", input_params=asdict(input_params))

        # pylint: disable=unexpected-keyword-arg
        self.repo.delete(input_params.id)

        if self.logger:
            self.logger.info("delete.category.usecase", message="Entity deleted")
