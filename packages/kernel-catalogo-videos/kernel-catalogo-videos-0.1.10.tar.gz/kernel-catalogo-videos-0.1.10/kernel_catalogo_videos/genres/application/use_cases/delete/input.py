"""
Input para deletar um genero
"""

# Python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DeleteGenreInput:
    id: str  # pylint: disable=invalid-name
