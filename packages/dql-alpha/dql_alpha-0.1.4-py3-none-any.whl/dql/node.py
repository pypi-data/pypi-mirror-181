import os
import posixpath
from datetime import datetime
from typing import List, NamedTuple, Optional

from dql.utils import time_to_str


class NodeRecord(NamedTuple):
    dir_id: Optional[str] = None
    parent_id: Optional[str] = None
    name: Optional[str] = None
    checksum: str = ""
    etag: str = ""
    version: Optional[str] = None
    is_latest: bool = True
    last_modified: datetime = datetime.now()
    size: int = 0
    owner_name: str = ""
    owner_id: str = ""
    anno: Optional[str] = None


_fields = list(NodeRecord.__annotations__.items())  # pylint:disable=no-member
NodeRecordWithPath = NamedTuple(  # type: ignore
    "NodeRecordWithPath",
    _fields + [("path", List[str])],
)


class AbstractNode:
    # pylint: disable=no-member
    TIME_FMT = "%Y-%m-%d %H:%M"

    @property
    def is_dir(self):
        return self.dir_id is not None

    @property
    def dir_id(self):
        return self.dir_id

    @property
    def name(self):
        return self.name

    @property
    def name_no_ext(self):
        name, _ = os.path.splitext(self.name)
        return name

    @property
    def dir_id_sql(self):
        return self.dir_id if (self.dir_id is not None) else "NULL"

    @property
    def equalis_dir_id_sql(self):
        return f" = {self.dir_id}" if (self.dir_id is not None) else " IS NULL"

    @property
    def is_downloadable(self):
        return not self.is_dir and self.name

    @property
    def size(self):
        return self.size or 0

    def get_metafile_data(self):
        data = {
            "name": "/".join(self.path),
            "etag": self.etag,
        }
        checksum = self.checksum
        if checksum:
            data["checksum"] = checksum
        version = self.version
        if version:
            data["version"] = version
        data["last_modified"] = time_to_str(self.last_modified)
        data["size"] = self.size
        return data

    def append_to_file(self, fd):
        fd.write(f"- name: {'/'.join(self.path)}\n")
        fd.write(f"  etag: {self.etag}\n")
        checksum = self.checksum
        if checksum:
            fd.write(f"  checksum: {self.checksum}\n")
        version = self.version
        if version:
            fd.write(f"  version: {self.version}\n")
        fd.write(f"  last_modified: '{time_to_str(self.last_modified)}'\n")
        size = self.size
        fd.write(f"  size: {self.size}\n")
        return size

    @property
    def full_path(self):
        path = posixpath.join(*self.path) if self.path else ""
        if self.is_dir and path:
            path += "/"
        return path

    def long_line_str(self):
        timestamp = self.last_modified if not self.is_dir else None
        return long_line_str(
            self.name_with_dir_ending, timestamp, self.owner_name
        )

    @property
    def name_with_dir_ending(self):
        ending = "/" if self.is_dir else ""
        return self.name + ending

    def print_line(self, long_format=False):
        if long_format:
            print(self.long_line_str())
        else:
            print(self.name_with_dir_ending)

    def sql_schema(self):
        return ",".join(["?"] * len(self))


class Node(NodeRecord, AbstractNode):
    pass


class NodeWithPath(  # pylint:disable=inherit-non-class
    NodeRecordWithPath,
    AbstractNode,
):
    pass


def long_line_str(name: str, timestamp: Optional[datetime], owner: str):
    if timestamp is None:
        time = "-"
    else:
        time = timestamp.strftime(AbstractNode.TIME_FMT)
    return f"{owner: <19} {time: <19} {name}"
