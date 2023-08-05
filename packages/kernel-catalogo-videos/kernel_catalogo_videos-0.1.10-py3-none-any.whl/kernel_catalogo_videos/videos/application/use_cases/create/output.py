"""
Input para retornar um video
"""

# Python
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.videos.application.use_cases.dto import VideoOutputDTO


@dataclass(slots=True, frozen=True)
class CreateVideoOutput(VideoOutputDTO):
    pass
