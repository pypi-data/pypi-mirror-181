"""
Buscar uma  categoria
"""
# pylint: disable=duplicate-code
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.entities import Category
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository
from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputMapper
from kernel_catalogo_videos.categories.application.use_cases.get.input import GetCategoryInput
from kernel_catalogo_videos.categories.application.use_cases.get.output import GetCategoryOutput


class GetCategoryUseCase(UseCase[GetCategoryInput, GetCategoryOutput]):
    """
    Classe para criar uma categoria
    """

    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: GetCategoryInput) -> GetCategoryOutput:
        if self.logger:
            self.logger.info("get.category.usecase", message="Initial Payload", input_params=asdict(input_params))

        category = self.repo.find_by_id(input_params.id)

        if self.logger:
            self.logger.info("get.category.usecase", message="Entity founded")

        return self.__to_output(category=category)

    def __to_output(self, category: Category):
        return CategoryOutputMapper.to_output(klass=GetCategoryOutput, category=category)
