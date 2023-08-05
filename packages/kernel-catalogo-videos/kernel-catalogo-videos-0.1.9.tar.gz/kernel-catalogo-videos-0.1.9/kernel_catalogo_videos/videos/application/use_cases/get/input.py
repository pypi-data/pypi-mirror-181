"""
Input para buscar um genero
"""

# Python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetVideoInput:
    id: str  # pylint: disable=invalid-name
