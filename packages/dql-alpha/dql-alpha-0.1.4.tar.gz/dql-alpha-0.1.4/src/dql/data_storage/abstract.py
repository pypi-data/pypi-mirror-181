import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from dql.node import Node, NodeWithPath
from dql.storage import Storage

DB_FILE_NAME = "db"


logger = logging.getLogger("dql")


class AbstractDataStorage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def clone(self, storage: Storage) -> "AbstractDataStorage":
        """Clones DataStorage implementation for some Storage input"""

    @abstractmethod
    def init_db(self):
        """Initializes database tables for data storage"""

    @abstractmethod
    def insert(self, values: List[Dict[str, Any]], **kwargs) -> None:
        """Inserts file or directory node into the database"""

    @abstractmethod
    def get_dir(self, parent_id: str, name: str) -> Optional[str]:
        """Gets directory id from database by name and parent_id"""

    @abstractmethod
    def upsert_storage(self, storage: Storage) -> None:
        """
        Saves new storage if it doesn't exist in database, otherwise it updates
        basic fields
        """

    @abstractmethod
    def register_storage_for_indexing(self, storage: Storage) -> None:
        """
        Prepares storage for indexing operation.
        This method should be called before index operation is started
        """

    @abstractmethod
    def mark_storage_indexed(self, storage: Storage, ttl: int) -> None:
        """
        Marks storage as indexed.
        This method should be called when index operation is finished
        """

    @abstractmethod
    def insert_root(self, storage: Storage) -> int:
        """
        Inserts root directory for some storage.
        It returns directory id of a newly created root
        """

    @abstractmethod
    def get_storage_all(self) -> Iterator[Storage]:
        pass

    @abstractmethod
    def get_storage(
        self, storage_id: str, expires_at: str
    ) -> Optional[Storage]:
        """
        Gets storage representation from database.
        E.g if s3 is used as storage this would be s3 bucket data
        """

    @abstractmethod
    def size(self, node: NodeWithPath, inames=None) -> Tuple[float, int]:
        """
        Calculates size of some node (and subtree below node).
        It can be filtered out by inames.
        Returns size in bytes as float and total files as int
        """

    @abstractmethod
    def get_node_by_path(self, path: str) -> NodeWithPath:
        """Gets node that correspond to some path"""

    @abstractmethod
    def get_nodes_by_path(self, path: str) -> Iterable[NodeWithPath]:
        """
        Gets all nodes that correspond to some path. Note that path
        can have GLOB like patterns so multiple nodes can be returned. If
        path is strict (without GLOB patterns) only one node will be returned.
        """

    @abstractmethod
    def get_latest_files_by_parent_node(
        self, parent_node: Node
    ) -> Iterable[Node]:
        """
        Gets file nodes that are latest version and have some parent node
        """

    @abstractmethod
    def walk_subtree(
        self,
        node: Node,
        filter="",  # pylint: disable=redefined-builtin
        jmespath="",
        sort_by_size=False,
        sort_by_name=False,
    ) -> Iterable[NodeWithPath]:
        """
        Returns all directory and file nodes that are "below" some node.
        Filters can be used for filtering some properties in nodes and jmespath
        as well.
        """

    @abstractmethod
    def walk_subtree_files_sorted_by_dir(
        self, node: NodeWithPath
    ) -> Iterable[NodeWithPath]:
        """
        Returns all directory and file nodes that are "below" some node
        sorted by parent ids
        """

    @abstractmethod
    def find(
        self,
        node: Node,
        names=None,
        inames=None,
        type=None,  # pylint: disable=redefined-builtin
        jmespath="",
    ) -> Iterable[NodeWithPath]:
        """
        Tries to find nodes that match certain criteria like name or jmespath
        """

    @abstractmethod
    def update_annotation(self, node: Node, annotation_content: str) -> None:
        """Updates annotation of a specific node in database"""

    @abstractmethod
    def update_checksum(self, node: Node, checksum: str) -> None:
        """Updates checksum of specific node in database"""
