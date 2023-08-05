"""
Caso de uso para criar uma categoria
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre
from kernel_catalogo_videos.genres.domain.factories import GenreFactory
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.services import CategoryService
from kernel_catalogo_videos.genres.domain.repositories import GenreRepository
from kernel_catalogo_videos.genres.application.use_cases.dto import GenreOutputMapper
from kernel_catalogo_videos.genres.application.use_cases.create.input import CreateGenreInput
from kernel_catalogo_videos.genres.application.use_cases.create.output import CreateGenreOutput


class CreateGenreUseCase(UseCase[CreateGenreInput, CreateGenreOutput]):
    """
    Classe para criar um genero
    """

    repo: GenreRepository

    def __init__(self, repo: GenreRepository, category_service: CategoryService, logger: Logger | None = None) -> None:
        self.repo = repo
        self.category_service = category_service
        self.logger = logger

    def save(self, entity):
        self.repo.insert(entity)
        if self.logger:
            self.logger.info("create.genre.usecase", message="Entity saved")

    def check_categories(self, input_params: CreateGenreInput):
        self.category_service.check_categories_exists(categories_uuid=input_params.categories)
        self.category_service.check_categories_is_inactive(categories_uuid=input_params.categories)
        self.category_service.check_categories_is_deleted(categories_uuid=input_params.categories)

    def execute(self, input_params: CreateGenreInput) -> CreateGenreOutput:
        if self.logger:
            self.logger.info("create.genre.usecase", message="Initial Payload", input_params=asdict(input_params))

        self.check_categories(input_params=input_params)

        genre_entity = GenreFactory(logger=self.logger).create(
            categories=input_params.categories, title=input_params.title, status=input_params.status
        )

        self.save(genre_entity)

        return self.__to_output(genre=genre_entity)

    def __to_output(self, genre: Genre):
        return GenreOutputMapper.to_output(klass=CreateGenreOutput, genre=genre)
