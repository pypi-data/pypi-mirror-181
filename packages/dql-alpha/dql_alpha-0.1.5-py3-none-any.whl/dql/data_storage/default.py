import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

import duckdb
import pandas as pd

from dql import utils
from dql.data_storage.abstract import AbstractDataStorage
from dql.error import DQLError
from dql.jmes_sql.transpiler import Transpiler
from dql.node import Node, NodeWithPath
from dql.storage import Storage
from dql.utils import DQL_PATH, GLOB_CHARS, sql_file_filter

DB_FILE_NAME = "db"


logger = logging.getLogger("dql")


class DefaultDataStorage(AbstractDataStorage):
    """
    Default data storage uses DuckDB for storing listing locally in file.
    Idea is to use it for cli and for other library clients to implement their
    own implementation although in theory they can use this one as well.
    """

    table_name = ""

    def __init__(self, db_file=None, table_name: str = ""):
        self.table_name = table_name
        self.db_file = db_file
        if not db_file:
            if not os.path.isdir(DQL_PATH):
                print("Creating '.dql/' directory")
                os.mkdir(DQL_PATH)
            db_file = os.path.join(DQL_PATH, DB_FILE_NAME)

        try:
            self.db = duckdb.connect(  # pylint:disable=c-extension-no-member
                database=db_file,
                read_only=False,
            )
            self._init_storage_table()
        except RuntimeError:
            raise DQLError("Cannot connect to DB")

    def _init_storage_table(self):
        """Initialize only tables related to storage, e.g s3"""
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS buckets
            (
                id          VARCHAR,
                type        VARCHAR,
                name        VARCHAR,
                timestamp   DATETIME,
                expires     DATETIME
            )
        """
        )

    def _sorting_by_name_or_size_sql(
        self, sort_by_name: bool, sort_by_size: bool
    ) -> str:
        """Creates sorting sql command by name OR size"""
        if sort_by_name and sort_by_size:
            raise RuntimeError(
                "Error: sorting by size and name at the same time"
            )
        if sort_by_size:
            sorting = "ORDER BY size DESC"
        elif sort_by_name:
            sorting = "ORDER BY path"
        else:
            sorting = ""
        return sorting

    def _get_nodes_by_glob_path_pattern(
        self, path_list: List[str], glob_name: str
    ) -> Iterable[NodeWithPath]:
        """Finds all Nodes that correspond to GLOB like path pattern."""
        node = self._get_node_by_path_list(path_list)
        if node.dir_id is None:  # type: ignore [attr-defined]
            raise RuntimeError(f"cannot resolve name {'/'.join(path_list)}")
        result = self.db.execute(
            f"""
            SELECT * FROM '{self.table_name}'
            WHERE parent_id = ? AND is_latest
                AND name GLOB ?
            """,
            [node.dir_id, glob_name],
        ).fetchall()
        return (
            NodeWithPath(*row, path_list)  # type: ignore [call-arg]
            for row in result
        )

    def _get_node_by_path_list(self, path_list: List[str]) -> NodeWithPath:
        """
        Gets node that correspond some path list,
        e.g ["data-lakes", "dogs-and-cats"]
        """
        all_fields = ", ".join(Node._fields)
        query = f"""
        WITH RECURSIVE FindDir AS
            (
                SELECT *, ? as path
                    FROM {self.table_name}
                    WHERE dir_id == 0
                UNION ALL
                SELECT t.*,
                       f.path[2:LEN(f.path)] AS path
                    FROM {self.table_name} t
                    JOIN FindDir f
                    ON t.parent_id = f.dir_id
                    WHERE t.name = f.path[1] AND t.is_latest
            )
            SELECT {all_fields}
                FROM FindDir
                WHERE path = []
        """
        res = self.db.execute(query, [path_list]).fetchall()
        if not res:
            path_str = os.path.join(*path_list)
            raise FileNotFoundError(f"Unable to resolve path {path_str}")
        assert len(res) == 1, "Error while resolving path"

        return NodeWithPath(*res[0], path_list)  # type: ignore [call-arg]

    def _populate_nodes_by_path(
        self, path_list: List[str], num: int, res: List[NodeWithPath]
    ) -> None:
        """
        Puts all nodes found by path_list into the res input variable.
        Note that path can have GLOB like pattern matching which means that
        res can have multiple nodes as result.
        If there is no GLOB pattern, res should have one node as result that
        match exact path by path_list
        """
        if num >= len(path_list):
            res.append(self._get_node_by_path_list(path_list))
            return

        curr_name = path_list[num]
        if set(curr_name).intersection(GLOB_CHARS):
            nodes = self._get_nodes_by_glob_path_pattern(
                path_list[:num], curr_name
            )
            for node in nodes:
                if not node.is_dir:
                    res.append(node)
                else:
                    path = (
                        path_list[:num]
                        + [node.name]
                        + path_list[num + 1 :]  # type: ignore [attr-defined]
                    )
                    self._populate_nodes_by_path(path, num + 1, res)
        else:
            self._populate_nodes_by_path(path_list, num + 1, res)
            return
        return

    def _get_jmespath_sql(self, jmespath: str) -> Optional[str]:
        """Returns sql representation of jmespath query"""
        if not jmespath:
            return None
        if len(jmespath) > 1:
            raise ValueError("multiple jmespath filters are not supported")
        try:
            jmespath_sql = Transpiler.build_sql(
                jmespath[0], "WalkTree", "anno", NodeWithPath._fields
            )
        except Exception as ex:
            raise ValueError("jmespath parsing error - " + str(ex))
        return jmespath_sql

    def clone(self, storage: Optional[Storage] = None) -> "DefaultDataStorage":
        if not storage:
            table_name = self.table_name
        else:
            table_name = storage.id
        ds = DefaultDataStorage(db_file=self.db_file, table_name=table_name)
        ds.db = self.db.duplicate()
        return ds

    def init_db(self):
        seq_name = "seq_" + self.table_name
        self.db.execute(
            f"""
            DROP TABLE IF EXISTS {self.table_name};
            DROP SEQUENCE IF EXISTS {seq_name};

            CREATE TABLE {self.table_name}
            (
                dir_id          UINTEGER,
                parent_id       UINTEGER,
                name            VARCHAR NOT NULL,
                checksum        VARCHAR,
                etag            VARCHAR,
                version         VARCHAR,
                is_latest       BOOL,
                last_modified   DATETIME,
                size            UBIGINT NOT NULL,
                owner_name      VARCHAR,
                owner_id        VARCHAR,
                anno            JSON
            );
            CREATE SEQUENCE {seq_name} START 1;

            CREATE TABLE IF NOT EXISTS buckets
            (
                id          VARCHAR,
                type        VARCHAR,
                name        VARCHAR,
                timestamp   DATETIME,
                expires     DATETIME
            )
        """
        )

    def _insert_files(self, files: List[Dict[str, Any]]) -> None:
        # remove path since it is not needed for DuckDB implementation
        for f in files:
            if "path" in f:
                del f["path"]
        df = pd.DataFrame(files)  # noqa: F841 #pylint: disable=unused-variable
        self.db.execute(f"INSERT INTO {self.table_name} SELECT * FROM df")

    def _insert_directories(self, directories: List[Dict[str, Any]]) -> None:
        # TODO: use a dataframe for insertion
        for d in directories:
            dir_id = d.get("dir_id")
            values = [
                d.get("parent_id"),
                d.get("name") or "",
                d.get("checksum"),
                d.get("etag"),
                d.get("version"),
                d.get("is_latest", True),
                d.get("last_modified"),
                d.get("size", 0),
                d.get("owner_name"),
                d.get("owner_id"),
                d.get("anno"),
            ]
            if dir_id is None:
                self.db.execute(
                    f"""
                    INSERT INTO {self.table_name} VALUES(
                        nextval('seq_{self.table_name}'),
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    values,
                )
            else:
                self.db.execute(
                    f"""
                    INSERT INTO {self.table_name} VALUES(
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    [dir_id, *values],
                )

    def insert(self, values: List[Dict[str, Any]], **kwargs) -> None:
        if kwargs.get("is_dir", False):
            self._insert_directories(values)
        else:
            self._insert_files(values)

    def get_dir(self, parent_id: str, name: str) -> Optional[str]:
        res = self.db.execute(
            f"""
            SELECT dir_id
            FROM {self.table_name}
            WHERE parent_id = ? AND name = ?
            """,
            [parent_id, name],
        ).fetchall()
        if res and res[0]:
            return res[0][0]

        return None

    def insert_root(self, storage: Storage) -> int:
        self.insert([{"dir_id": 0}], is_dir=True, is_root=True)
        # root in DuckDB has always zero id
        return 0

    def get_storage_all(self) -> Iterator[Storage]:
        for values in self.db.execute("SELECT * FROM buckets").fetchall():
            yield Storage(*values)

    def get_storage(
        self, storage_id: str, expires_at: str
    ) -> Optional[Storage]:
        res = self.db.execute(
            """
            SELECT * FROM buckets
            WHERE id = ? AND expires > ?
            """,
            [storage_id, expires_at],
        ).fetchall()
        if not res:
            return None

        assert len(res) == 1, f"Storage duplication: {storage_id}"

        return Storage(*res[0])

    def size(self, node: NodeWithPath, inames=None) -> Tuple[float, int]:
        def _nullable_to_sql_condition(
            _id: str,
        ) -> str:  # pylint:disable=redefined-builtin
            return f" ={_id}" if _id is not None else " IS NULL"

        dir_id_cond = _nullable_to_sql_condition(
            node.dir_id  # type: ignore [attr-defined]
        )
        parent_id_cond = _nullable_to_sql_condition(
            node.parent_id  # type: ignore [attr-defined]
        )
        sql_filter = None
        if inames:
            # filter out only json files
            sql_filter = utils.sql_file_filter(inames=["*.json"])

        # ToDo: total_files should include ONLY files not dirs
        res = self.db.execute(
            f"""
            WITH RECURSIVE FileTreeWalkWithSize AS
            (
                SELECT *,
                       size AS total_size,
                       IF(dir_id IS NULL, 1, 0) AS total_files
                    FROM {self.table_name}
                    WHERE dir_id {dir_id_cond} AND parent_id {parent_id_cond}
                            AND name = ? AND is_latest
                UNION ALL
                SELECT t.*,
                       t.size + w.size AS total_size,
                       IF(t.dir_id IS NULL, 1, 0) + w.total_files AS total_files
                    FROM {self.table_name} t
                    JOIN FileTreeWalkWithSize w
                    ON t.parent_id = w.dir_id
                    WHERE t.is_latest
            )
            SELECT SUM(total_size), SUM(total_files)
                FROM FileTreeWalkWithSize
                {"WHERE " + sql_filter if sql_filter else ""}
            """,  # noqa: E501
            [node.name],
        ).fetchall()
        assert len(res) == 1, "du - unexpected result in sql query"

        return res[0][0], res[0][1]

    def upsert_storage(self, storage: Storage) -> None:
        res = self.db.execute(
            """SELECT * FROM buckets WHERE id = ?""", [storage.id]
        ).fetchall()

        old_storage = Storage(*res[0]) if res and len(res) == 1 else None

        self.db.execute(
            f"""
            DELETE FROM buckets WHERE id = '{storage.id}';
            INSERT INTO buckets VALUES(?, ?, ?, ?, ?)
            """,
            [
                storage.id,
                storage.type,
                storage.name,
                old_storage.timestamp if old_storage else None,
                old_storage.expires if old_storage else None,
            ],
        )

    def register_storage_for_indexing(self, storage: Storage) -> None:
        self.upsert_storage(storage)
        self.db.execute(
            """
            UPDATE buckets
            SET timestamp = ?, expires = ?
            WHERE id = ?
            """,
            [
                None,
                None,
                storage.id,
            ],
        )

    def mark_storage_indexed(self, storage: Storage, ttl: int) -> None:
        timestamp = datetime.now(timezone.utc)
        self.db.execute(
            """
            UPDATE buckets
            SET timestamp = ?, expires = ?
            WHERE id = ?
            """,
            [
                timestamp,
                Storage.get_expiration_time(timestamp, ttl),
                storage.id,
            ],
        )

    def get_node_by_path(self, path: str) -> NodeWithPath:
        path = path.lstrip("/")

        is_dir_required = False
        if path and path[-1] == "/":
            path = path.rstrip("/")
            is_dir_required = True

        path_list = path.split("/") if path != "" else []
        node = self._get_node_by_path_list(path_list)

        if is_dir_required and not node.is_dir:
            raise FileNotFoundError(f"Directory {path} is not found")

        return node

    def get_nodes_by_path(self, path: str) -> Iterable[NodeWithPath]:
        clean_path = path.strip("/")
        path_list = clean_path.split("/") if clean_path != "" else []

        res: List[NodeWithPath] = []
        self._populate_nodes_by_path(path_list, 0, res)
        return res

    def get_latest_files_by_parent_node(
        self, parent_node: Node
    ) -> Iterable[Node]:
        if not parent_node.is_dir:
            return [parent_node]

        result = self.db.execute(
            f"""
            SELECT * FROM '{self.table_name}'
            WHERE parent_id = ? AND is_latest
            """,
            [parent_node.dir_id],
        ).fetchall()
        return map(Node._make, result)

    def walk_subtree(
        self,
        node: Node,
        filter="",  # pylint: disable=redefined-builtin
        jmespath="",
        sort_by_size=False,
        sort_by_name=False,
    ) -> Iterable[NodeWithPath]:
        sorting_sql = self._sorting_by_name_or_size_sql(
            sort_by_name, sort_by_size
        )
        name_filter_sql = "WHERE " + filter if filter else ""

        walktree_sql = f"""
            CREATE OR REPLACE TEMP VIEW WalkTree AS (
                WITH RECURSIVE FileTreeWalk AS
                (
                    SELECT *, [name] AS path
                        FROM {self.table_name}
                        WHERE parent_id = {node.dir_id} AND is_latest
                    UNION ALL
                    SELECT t.*, list_append(w.path, t.name)
                        FROM {self.table_name} t
                        JOIN FileTreeWalk w
                        ON t.parent_id = w.dir_id
                        WHERE t.is_latest
                )
                SELECT *
                    FROM FileTreeWalk {name_filter_sql} {sorting_sql}
            )
            """

        jmespath_sql = self._get_jmespath_sql(jmespath)
        if jmespath_sql:
            sql = walktree_sql + ";" + jmespath_sql
        else:
            sql = walktree_sql + "; SELECT * FROM WalkTree"

        cursor = self.db.execute(sql)

        row = cursor.fetchone()
        while row:
            yield NodeWithPath(*row)
            row = cursor.fetchone()

    def walk_subtree_files_sorted_by_dir(
        self, node: NodeWithPath
    ) -> Iterable[NodeWithPath]:
        cursor = self.db.execute(
            f"""
            WITH RECURSIVE FileTreeWalk AS
            (
                SELECT *, [name] AS path
                    FROM {self.table_name}
                    WHERE parent_id = ? AND is_latest
                UNION ALL
                SELECT t.*, list_append(w.path, t.name)
                    FROM {self.table_name} t
                    JOIN FileTreeWalk w
                    ON t.parent_id = w.dir_id
                    WHERE t.is_latest
            )
            SELECT *
                FROM FileTreeWalk
                WHERE dir_id IS NULL
                ORDER BY parent_id
            """,
            [node.dir_id],
        )

        row = cursor.fetchone()
        while row:
            yield NodeWithPath(*row)
            row = cursor.fetchone()

    def find(
        self,
        node: Node,
        names=None,
        inames=None,
        type=None,  # pylint: disable=redefined-builtin
        jmespath="",
    ) -> Iterable[NodeWithPath]:
        name_filter = utils.sql_file_filter(names, inames, type)
        return self.walk_subtree(node, filter=name_filter, jmespath=jmespath)

    def update_annotation(self, node: Node, annotation_content: str) -> None:
        img_exts = ["jpg", "jpeg", "png"]
        names = (node.name_no_ext + "." + ext for ext in img_exts)
        filter_sql = sql_file_filter(inames=names, op="=")

        try:
            res = self.db.execute(
                f"""
                UPDATE '{self.table_name}'
                SET anno = ?
                WHERE dir_id ?
                    AND parent_id = ?
                    AND is_latest
                    AND {filter_sql}
                """,
                [annotation_content, node.equalis_dir_id_sql, node.parent_id],
            ).fetchall()

            if res is None or len(res) == 0:
                msg = f"no image file was found for annotation {node.name}"
                logger.warning(msg)
            elif res[0][0] > 1:
                msg = (
                    f"multiple image files were updated for a single "
                    f"annotation {node.name}"
                )
                logger.warning(msg)
        except duckdb.ParserException:  # pylint:disable=c-extension-no-member
            msg = f"unable to parse json annotation for file {node.name}"
            logger.warning(msg)

    def update_checksum(self, node: Node, checksum: str) -> None:
        args = [checksum]
        conditions = []
        for field_name, value in [
            ("dir_id", node.dir_id),
            ("parent_id", node.parent_id),
            ("version", node.version),
            ("name", node.name),
        ]:
            if value is None:
                conditions.append(f"{field_name} IS NULL")
            else:
                conditions.append(f"{field_name} = ?")
                args.append(value)
        cond_str = " AND ".join(conditions)
        self.db.execute(
            f"""
            UPDATE '{self.table_name}'
            SET checksum = ?
            WHERE {cond_str}
            """,
            args,
        )
