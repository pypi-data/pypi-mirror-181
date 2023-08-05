import concurrent.futures
import multiprocessing
import os
import threading
from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, Iterator, Tuple, Type

from tqdm import tqdm

from dql.client.base import Bucket, Client
from dql.data_storage import AbstractDataStorage
from dql.listing import Listing
from dql.nodes_fetcher import NodesFetcher
from dql.nodes_thread_pool import NodeChunk

if TYPE_CHECKING:
    from fsspec.spec import AbstractFileSystem


class FSSpecClient(Client):
    THREAD_LOCK = threading.Lock()
    MAX_THREADS = multiprocessing.cpu_count()
    MAX_THREADS_LISTING = int(
        os.environ.get("MAX_THREADS_LISTING", MAX_THREADS * 10)
    )
    CHUNK_SIZE = 1024 * 1024
    FS_CLASS: ClassVar[Type["AbstractFileSystem"]]
    PREFIX: ClassVar[str]

    def __init__(self, name, fs):
        self.name = name
        self.fs = fs
        self.lock = threading.Lock()
        self.global_counter = 0

    @classmethod
    def create_fs(cls, **kwargs) -> "AbstractFileSystem":
        kwargs.setdefault("version_aware", True)
        return cls.FS_CLASS(**kwargs)

    @classmethod
    def ls_buckets(cls, **kwargs) -> Iterator[Bucket]:
        for entry in cls.create_fs(**kwargs).ls(cls.PREFIX, detail=True):
            yield Bucket(
                name=entry["name"],
                uri=f'{cls.PREFIX}{entry["name"]}',
                created=entry.get("CreationDate"),
            )

    @classmethod
    def is_root_url(cls, url) -> bool:
        return url == cls.PREFIX

    @property
    def uri(self):
        return f"{self.PREFIX}{self.name}"

    @classmethod
    def _parse_url(
        cls,
        source: str,
        **kwargs,
    ) -> Tuple["FSSpecClient", str]:
        """
        Returns storage representation of bucket and the rest of the path
        in source.
        E.g if the source is s3://bucket_name/dir1/dir2/dir3 this method would
        return Storage object of bucket_name and a path which is dir1/dir2/dir3
        """
        fill_path = source[len(cls.PREFIX) :]
        path_split = fill_path.split("/", 1)
        storage = path_split[0]
        path = path_split[1] if len(path_split) > 1 else ""
        return cls(storage, **kwargs), path

    def fetch(self, listing):
        def initializer_worker(local, data_storage):
            """
            Adding cloned instance of data storage as thread local for each
            thread in thread pool so that we don't need to clone it for each
            task
            """
            local.data_storage = data_storage.clone()

        root_id = listing.insert_root()

        local = threading.local()
        # setting up data_storage for main thread
        local.data_storage = listing.data_storage

        with concurrent.futures.ThreadPoolExecutor(
            self.MAX_THREADS_LISTING,
            initializer=initializer_worker,
            initargs=(
                local,
                listing.data_storage,
            ),
        ) as executor:
            progress_bar = tqdm(desc=f"Listing {self.uri}", unit=" objects")
            tasks = self._fetch_dir(
                root_id,
                "",
                "/",
                executor,
                progress_bar,
                local,
            )
            while tasks:
                for task in concurrent.futures.as_completed(tasks):
                    tasks.remove(task)
                    tasks.update(task.result())

    def _fetch_dir(self, dir_id, prefix, delimiter, executor, pbar, local):
        data_storage = local.data_storage

        path = f"{self.name}/{prefix}"
        infos = self.fs.ls(path, detail=True, versions=True)
        files = []
        tasks = set()
        for info in infos:
            full_path = info["name"]
            _, subprefix, _ = self.fs.split_path(info["name"])
            if info["type"] == "directory":
                name = full_path.split(delimiter)[-1]
                new_dir_id = (
                    Listing._insert_dir(  # pylint:disable=protected-access
                        data_storage, dir_id, name, datetime.max, subprefix
                    )
                )

                task = executor.submit(
                    self._fetch_dir,
                    new_dir_id,
                    subprefix,
                    delimiter,
                    executor,
                    pbar,
                    local,
                )
                tasks.add(task)
            else:
                files.append(
                    self._df_from_info(info, dir_id, delimiter, subprefix)
                )
        if files:
            data_storage.insert(files, is_dir=False)
        self.update_pbar_threadsafe(pbar, len(infos))
        return tasks

    @classmethod
    @abstractmethod
    def _df_from_info(cls, v, dir_id, delimiter, path):
        ...

    @classmethod
    def update_pbar_threadsafe(cls, pbar, obj_num):
        with cls.THREAD_LOCK:
            pbar.update(obj_num)

    def fetch_nodes(
        self,
        file_path,
        nodes,
        cache,
        data_storage: AbstractDataStorage,
        total_size=None,
        cls=NodesFetcher,
        pb_descr="Download",
    ):
        fetcher = cls(
            self,
            data_storage,
            file_path,
            self.MAX_THREADS,
            cache,
        )

        chunk_gen = NodeChunk(nodes)
        target_name = self.visual_file_name(file_path)
        pb_descr = f"{pb_descr} {target_name}"
        return fetcher.run(chunk_gen, pb_descr, total_size)

    def iter_object_chunks(self, bucket, path, version=None):
        with self.fs.open(f"{bucket}/{path}", version_id=version) as f:
            chunk = f.read()
            while chunk:
                yield chunk
                chunk = f.read()

    @staticmethod
    def visual_file_name(file_path):
        target_name = file_path.rstrip("/").split("/")[-1]
        max_len = 25
        if len(target_name) > max_len:
            target_name = "..." + target_name[max_len - 3 :]
        return target_name
