"""
Output retornando os dados de uma categoria
"""
# pylint: disable=duplicate-code

# Python
from typing import TypeVar, Optional
from datetime import datetime
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.castmembers.domain.entities import CastMember


@dataclass(slots=True, frozen=True)
class CastMemberOutputDTO:
    id: str  # pylint: disable=invalid-name
    name: str
    kind: int
    is_deleted: bool
    created_at: datetime
    status: Optional[int] = 1


Output = TypeVar("Output", bound=CastMemberOutputDTO)


class CastMemberOutputMapper:
    @staticmethod
    def to_output(klass: Output, castmember: CastMember) -> Output:
        return klass(
            id=castmember.id,
            name=castmember.name,
            kind=castmember.kind,
            status=castmember.status,
            is_deleted=castmember.is_deleted,
            created_at=castmember.created_at,
        )
