"""
Retorna uma lista de membros
"""

# Apps
from kernel_catalogo_videos.core.application.dto import PaginationOutput
from kernel_catalogo_videos.castmembers.application.use_cases.dto import CastMemberOutputDTO


class SearchCastMemberOutput(PaginationOutput[CastMemberOutputDTO, str]):
    pass
