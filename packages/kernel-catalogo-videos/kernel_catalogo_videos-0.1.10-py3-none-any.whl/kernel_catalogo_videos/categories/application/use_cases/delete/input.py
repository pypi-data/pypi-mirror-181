"""
Input para deletar uma categoria
"""

# Python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DeleteCategoryInput:
    id: str  # pylint: disable=invalid-name
