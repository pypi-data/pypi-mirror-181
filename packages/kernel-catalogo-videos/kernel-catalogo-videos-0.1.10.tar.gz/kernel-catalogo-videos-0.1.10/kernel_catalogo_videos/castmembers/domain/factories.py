# Python
from logging import Logger

# Apps
from kernel_catalogo_videos.castmembers.domain.entities import CastMember


class CastMemberFactory:
    def __init__(self, logger: Logger | None = None) -> None:
        self.logger = logger

    def create(self, name: str, kind: str, status: int) -> CastMember:

        castmember = CastMember(name=name, kind=kind, status=status)

        if self.logger:
            self.logger.info("create.castmember.factory", message="Entity created", castmember=castmember.to_dict())

        return castmember
