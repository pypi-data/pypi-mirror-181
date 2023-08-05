import posixpath
from datetime import datetime, timedelta
from typing import NamedTuple, Optional

from dateutil import tz

from dql.node import Node
from dql.utils import time_to_str


class Status:
    CREATED = 1
    PENDING = 2
    FAILED = 3
    COMPLETE = 4


class StorageRecord(NamedTuple):
    id: str  # pylint:disable=redefined-builtin
    type: str  # pylint:disable=redefined-builtin
    name: str
    timestamp: Optional[datetime]
    expires: Optional[datetime]
    status: int = Status.CREATED


class Storage(StorageRecord):
    @property
    def root_node(self):
        return Node(0, None, self.name)

    @property
    def uri(self):
        return f"{self.type}://{self.name}"

    @property
    def timestamp_str(self) -> Optional[str]:
        if not self.timestamp:
            return None
        return time_to_str(self.timestamp)

    @property
    def timestamp_to_local(self) -> Optional[str]:
        if not self.timestamp:
            return None
        return self.time_to_local(self.timestamp)

    @property
    def expires_to_local(self) -> Optional[str]:
        if not self.expires:
            return None
        return self.time_to_local(self.expires)

    @staticmethod
    def time_to_local(dt: datetime) -> str:
        try:
            local = dt.astimezone(tz.tzlocal())
        except (OverflowError, OSError, ValueError):
            local = dt
        return time_to_str(local)

    @staticmethod
    def get_expiration_time(timestamp: datetime, ttl: int):
        if ttl >= 0:
            try:
                return timestamp + timedelta(seconds=ttl)
            except OverflowError:
                return datetime.max
        else:
            return datetime.max

    def to_dict(self, file_path=""):
        uri = self.uri
        if file_path:
            uri = posixpath.join(uri, *file_path.rstrip("/").split("/"))
        return {
            "uri": uri,
            "timestamp": time_to_str(self.timestamp)
            if self.timestamp
            else None,
            "expires": time_to_str(self.expires) if self.expires else None,
        }
