import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar, Iterator, NamedTuple, Optional, Tuple, Type

from funcy import cached_property

from dql.storage import Storage


class Bucket(NamedTuple):
    name: str
    uri: str
    created: Optional[datetime]


class Client(ABC):
    SHA_LIMIT = 12
    ID_PREFIX = "dsrc_"
    ID_LENGTH = SHA_LIMIT + len(ID_PREFIX)
    name: str
    protocol: ClassVar[str]

    @staticmethod
    def get_implementation(url: str) -> Type["Client"]:
        from .gcs import GCSClient
        from .s3 import ClientS3

        if url.startswith(ClientS3.PREFIX):
            return ClientS3
        if url.startswith(GCSClient.PREFIX):
            return GCSClient
        raise RuntimeError(f"Unsupported data source format '{url}'")

    @staticmethod
    def parse_url(source: str, **kwargs) -> Tuple["Client", str]:
        cls = Client.get_implementation(source)
        return cls._parse_url(  # pylint:disable=protected-access
            source, **kwargs
        )

    @classmethod
    @abstractmethod
    def is_root_url(cls, url) -> bool:
        ...

    @classmethod
    @abstractmethod
    def _parse_url(cls, source: str, **kwargs) -> Tuple["Client", str]:
        ...

    @classmethod
    @abstractmethod
    def ls_buckets(cls, **kwargs) -> Iterator[Bucket]:
        ...

    @property
    @abstractmethod
    def uri(self) -> str:
        ...

    @cached_property
    def storage_id(self):
        sha = hashlib.sha256(self.uri.encode("utf-8")).hexdigest()
        return Client.ID_PREFIX + sha[: Client.SHA_LIMIT]

    def as_record(self) -> Storage:
        return Storage(self.storage_id, self.protocol, self.name, None, None)
