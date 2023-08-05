# Python
from typing import List
from logging import Logger

# Apps
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository


class CategoryService:
    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def check_categories_exists(self, categories_uuid: List[str]):
        # TODO: Check categories exists
        if self.logger:
            self.logger.info(
                "services.category.check_categories_exists",
                message="Check categories exists",
                categories=categories_uuid,
            )

    def check_categories_is_inactive(self, categories_uuid: List[str]):
        # TODO: Check categories is inactive
        if self.logger:
            self.logger.info(
                "services.category.check_categories_is_inactive",
                message="Check categories exists",
                categories=categories_uuid,
            )

    def check_categories_is_deleted(self, categories_uuid: List[str]):
        # TODO: Check categories is deleted
        if self.logger:
            self.logger.info(
                "services.category.check_categories_is_deleted",
                message="Check categories is deleted",
                categories=categories_uuid,
            )
