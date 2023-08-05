"""
Input para buscar um membro
"""

# Python
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetCastMemberInput:
    id: str  # pylint: disable=invalid-name
