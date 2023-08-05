"""
Caso de uso para criar uma categoria
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.entities import Category
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository
from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputMapper
from kernel_catalogo_videos.categories.application.use_cases.create.input import CreateCategoryInput
from kernel_catalogo_videos.categories.application.use_cases.create.output import CreateCategoryOutput


class CreateCategoryUseCase(UseCase[CreateCategoryInput, CreateCategoryOutput]):
    """
    Classe para criar uma categoria
    """

    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: CreateCategoryInput) -> CreateCategoryOutput:
        if self.logger:
            self.logger.info("create.category.usecase", message="Initial Payload", input_params=asdict(input_params))

        category = Category(
            title=input_params.title,
            description=input_params.description,
            status=input_params.status,
        )
        category.normalize()
        if self.logger:
            self.logger.info("create.category.usecase", message="Entity created", category=category.to_dict())

        self.repo.insert(category)
        if self.logger:
            self.logger.info("create.category.usecase", message="Entity saved")

        return self.__to_output(category=category)

    def __to_output(self, category: Category):
        return CategoryOutputMapper.to_output(klass=CreateCategoryOutput, category=category)
