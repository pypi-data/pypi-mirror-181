"""
Modulo seedwork para uma Entidade
"""
# pylint: disable=duplicate-code

# Python
from abc import ABC
from dataclasses import Field, field, asdict, dataclass

# Apps
from kernel_catalogo_videos.core.domain.unique_entity_id import UniqueEntityId


@dataclass(kw_only=True, frozen=True)
class Entity(ABC):
    """
    Classe Entidade
    """

    unique_entity_id: UniqueEntityId = field(default_factory=UniqueEntityId)

    # pylint: disable=C0103
    @property
    def id(self):
        """
        Retorna o id do tipo UUID como string
        """
        return str(self.unique_entity_id)

    def to_dict(self):
        """
        Retorna um dicionario com o id como string
        """
        entity_dict = asdict(self)
        entity_dict.pop("unique_entity_id")
        entity_dict["id"] = self.id

        return entity_dict

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        # pylint: disable=no-member
        return cls.__dataclass_fields__[entity_field]

    def _set(self, field_name, value):
        object.__setattr__(self, field_name, value)

        return self
