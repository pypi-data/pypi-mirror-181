"""
Modulo seedwork representando um id do tipo UUID
"""
# Python
import uuid
from dataclasses import field, dataclass

# Apps
from kernel_catalogo_videos.core.utils import uuidv4
from kernel_catalogo_videos.core.domain.exceptions import InvalidUUIDException


@dataclass(frozen=True)
class UniqueEntityId:
    """
    Classe entidade representando um id como UUID
    """

    # pylint: disable=C0103
    id: str = field(default_factory=uuidv4)

    def __post_init__(self):
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, "id", id_value)
        self.__validate()

    def __validate(self):
        try:
            uuid.UUID(self.id)
        except ValueError as exc:
            raise InvalidUUIDException() from exc

    def __str__(self):
        return f"{self.id}"
