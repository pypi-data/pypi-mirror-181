"""
Input para criar um genero
"""
# Python
from typing import Optional
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.castmembers.domain.entities import CastMember


@dataclass(slots=True, frozen=True)
class CreateCastMemberInput:
    name: str
    kind: int = CastMember.get_field("kind").default
    status: Optional[int] = CastMember.get_field("status").default
