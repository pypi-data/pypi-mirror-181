"""
Define uma entidade
"""
# pylint: disable=duplicate-code


# Python
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import field, dataclass

# Third
from slugify import slugify

# Apps
from kernel_catalogo_videos.core.utils import ACTIVE_STATUS, INACTIVE_STATUS, now
from kernel_catalogo_videos.core.domain.entities import Entity


@dataclass(kw_only=True, frozen=True, slots=True)
class Genre(Entity):
    """
    Representa os dados da entidade genero
    """

    title: str
    categories: List[str]
    slug: Optional[str] = ""
    status: Optional[int] = ACTIVE_STATUS
    is_deleted: bool = False
    created_at: Optional[datetime] = field(default_factory=now)

    def __post_init__(self):
        self.normalize()

    def update(self, data: Dict[str, Any]):
        """
        Atualiza os dados internos da entidade
        """
        for field_name, value in data.items():
            self._set(field_name, value)

        self.normalize()

    def normalize(self):
        slugged = slugify(self.title)
        self._set("slug", slugged)

    def activate(self):
        """
        Seta o atributo status como ativo
        """
        self._set("status", ACTIVE_STATUS)

    def deactivate(self):
        """
        Seta o atributo status como inativo
        """
        self._set("status", INACTIVE_STATUS)
