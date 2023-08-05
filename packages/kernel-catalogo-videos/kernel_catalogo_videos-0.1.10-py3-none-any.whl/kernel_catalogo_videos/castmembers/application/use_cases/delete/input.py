"""
Input para deletar um membro
"""

# Python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DeleteCastMemberInput:
    id: str  # pylint: disable=invalid-name
