"""
Listar categorias
"""


# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.core.application.dto import PaginationOutputMapper
from kernel_catalogo_videos.core.domain.repositories import SearchParams, SearchResult
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository
from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputDTO, CategoryOutputMapper
from kernel_catalogo_videos.categories.application.use_cases.search.input import SearchCategoryInput
from kernel_catalogo_videos.categories.application.use_cases.search.output import SearchCategoryOutput


class SearchCategoriesUseCase(UseCase[SearchCategoryInput, SearchCategoryOutput]):
    """
    Classe para listar categorias
    """

    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: SearchCategoryInput) -> SearchCategoryOutput:
        if self.logger:
            self.logger.info("search.category.usecase", message="Initial Payload", input_params=asdict(input_params))

        search_params = SearchParams(**asdict(input_params))

        result = self.repo.search(params=search_params)

        if self.logger:
            self.logger.info("search.category.usecase", message="Entities listed")

        return self.__to_output(result=result)

    def __to_output(self, result: SearchResult):
        items = list(
            map(
                lambda category: CategoryOutputMapper.to_output(klass=CategoryOutputDTO, category=category),
                result.items,
            )
        )
        return PaginationOutputMapper.from_child(SearchCategoryOutput).to_output(items=items, result=result)
