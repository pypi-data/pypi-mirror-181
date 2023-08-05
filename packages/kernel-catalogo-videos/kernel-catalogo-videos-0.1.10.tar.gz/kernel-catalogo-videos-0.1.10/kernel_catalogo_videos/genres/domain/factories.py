# Python
from typing import List
from logging import Logger

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre


class GenreFactory:
    def __init__(self, logger: Logger | None = None) -> None:
        self.logger = logger

    def create(self, categories: List[str], title: str, status: int) -> Genre:

        genre = Genre(
            categories=categories,
            title=title,
            status=status,
        )
        genre.normalize()

        if self.logger:
            self.logger.info("create.genre.usecase", message="Entity created", genre=genre.to_dict())

        return genre
