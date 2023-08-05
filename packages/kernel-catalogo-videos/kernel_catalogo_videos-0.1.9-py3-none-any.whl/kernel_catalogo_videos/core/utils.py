# Python
import uuid
from typing import Any
from datetime import datetime, timezone

utc = timezone.utc

INACTIVE_STATUS = 0
ACTIVE_STATUS = 1

KIND_DIRECTOR = 0
KIND_ACTOR = 1


def now() -> datetime:
    return datetime.now(tz=utc)


def uuidv4() -> uuid.UUID:
    return uuid.uuid4()


def check_is_deleted(obj: Any):
    return obj.is_deleted is True


def check_is_inactive(obj: Any) -> bool:
    return obj.status == INACTIVE_STATUS


def check_is_inactive_or_deleted(obj: Any) -> bool:
    is_deleted = check_is_deleted(obj) if hasattr(obj, "is_deleted") else False
    is_inactive = check_is_inactive(obj) if hasattr(obj, "status") else False

    return is_inactive or is_deleted
