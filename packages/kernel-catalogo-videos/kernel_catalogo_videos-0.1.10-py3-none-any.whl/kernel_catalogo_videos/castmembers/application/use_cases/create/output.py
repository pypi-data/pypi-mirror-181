"""
Input para retornar um genero
"""

# Python
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.castmembers.application.use_cases.dto import CastMemberOutputDTO


@dataclass(slots=True, frozen=True)
class CreateCastMemberOutput(CastMemberOutputDTO):
    pass
