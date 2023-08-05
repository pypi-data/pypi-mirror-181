"""
Retorna uma lista de videos
"""

# Apps
from kernel_catalogo_videos.core.application.dto import PaginationOutput
from kernel_catalogo_videos.videos.application.use_cases.dto import VideoOutputDTO


class SearchVideoOutput(PaginationOutput[VideoOutputDTO, str]):
    pass
