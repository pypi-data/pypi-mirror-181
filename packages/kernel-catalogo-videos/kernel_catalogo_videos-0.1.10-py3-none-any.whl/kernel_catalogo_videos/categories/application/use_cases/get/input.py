"""
Input para buscar uma categoria
"""

# Python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetCategoryInput:
    id: str  # pylint: disable=invalid-name
