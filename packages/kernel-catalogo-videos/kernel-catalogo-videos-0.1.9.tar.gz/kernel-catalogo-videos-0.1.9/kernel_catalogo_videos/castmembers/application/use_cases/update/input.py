"""
Input para atualizar um genero
"""
# Python
from typing import Optional
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.castmembers.domain.entities import CastMember


@dataclass(slots=True, frozen=False)
class UpdateCastMemberInput:
    id: str  # pylint: disable=invalid-name
    name: str
    kind: int = CastMember.get_field("kind").default
    status: Optional[int] = CastMember.get_field("status").default
    is_deleted: Optional[bool] = CastMember.get_field("is_deleted").default
