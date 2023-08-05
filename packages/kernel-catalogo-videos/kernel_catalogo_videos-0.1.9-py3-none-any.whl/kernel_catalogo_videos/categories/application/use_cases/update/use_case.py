"""
Caso de uso para atualizar uma categoria
"""
# pylint: disable=duplicate-code

# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.utils import ACTIVE_STATUS, INACTIVE_STATUS
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.entities import Category
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository
from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputMapper
from kernel_catalogo_videos.categories.application.use_cases.update.input import UpdateCategoryInput
from kernel_catalogo_videos.categories.application.use_cases.update.output import UpdateCategoryOutput


class UpdateCategoryUseCase(UseCase[UpdateCategoryInput, UpdateCategoryOutput]):
    """
    Atualizar uma categoria
    """

    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: UpdateCategoryInput) -> UpdateCategoryOutput:
        if self.logger:
            self.logger.info("update.category.usecase", message="Initial Payload", input_params=asdict(input_params))

        entity = self.repo.find_by_id(input_params.id)

        if self.logger:
            self.logger.info("update.category.usecase", message="Founded entity", entity=entity.to_dict())

        entity.update(data={"title": input_params.title, "description": input_params.description})

        if input_params.status == ACTIVE_STATUS:
            entity.activate()

        if input_params.status == INACTIVE_STATUS:
            entity.deactivate()

        if self.logger:
            self.logger.info("update.category.usecase", message="Entity updated", entity=entity.to_dict())

        self.repo.update(entity=entity)
        if self.logger:
            self.logger.info("create.category.usecase", message="Entity saved")

        return self.__to_output(category=entity)

    def __to_output(self, category: Category):
        return CategoryOutputMapper.to_output(klass=UpdateCategoryOutput, category=category)
