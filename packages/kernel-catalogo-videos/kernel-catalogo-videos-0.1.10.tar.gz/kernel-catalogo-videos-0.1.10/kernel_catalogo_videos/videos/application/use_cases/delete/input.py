"""
Input para deletar um video
"""

# Python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DeleteVideoInput:
    id: str  # pylint: disable=invalid-name
