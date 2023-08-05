"""
Input para retornar um genero
"""

# Python
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.videos.application.use_cases.dto import VideoOutputDTO


@dataclass(slots=True, frozen=True)
class UpdateVideoOutput(VideoOutputDTO):
    pass
