import os
import os.path as osp
import stat
from typing import Iterable, Optional, Type, TypeVar

GLOB_CHARS = ["?", "*", "[", "]"]

T = TypeVar("T", bound="DQLDir")


class DQLDir:
    DEFAULT = ".dql"
    CACHE = "cache"
    TMP = "tmp"
    DB = "db"
    ENV_VAR = "DQL_DIR"

    def __init__(
        self,
        root: Optional[str] = None,
        cache: Optional[str] = None,
        tmp: Optional[str] = None,
        db: Optional[str] = None,
    ) -> None:
        self.root = (
            osp.abspath(root) if root is not None else self.default_root()
        )
        self.cache = (
            osp.abspath(cache)
            if cache is not None
            else osp.join(self.root, self.CACHE)
        )
        self.tmp = (
            osp.abspath(tmp)
            if tmp is not None
            else osp.join(self.root, self.TMP)
        )
        self.db = (
            osp.abspath(db) if db is not None else osp.join(self.root, self.DB)
        )

    def init(self):
        os.makedirs(self.root, exist_ok=True)
        os.makedirs(self.cache, exist_ok=True)
        os.makedirs(self.tmp, exist_ok=True)
        os.makedirs(osp.split(self.db)[0], exist_ok=True)

    @classmethod
    def default_root(cls) -> str:
        return osp.join(os.getcwd(), cls.DEFAULT)

    @classmethod
    def find(cls: Type[T], create: bool = True) -> T:
        try:
            root = os.environ[cls.ENV_VAR]
        except KeyError:
            root = cls.default_root()
        instance = cls(root)
        if not osp.isdir(root):
            if create:
                instance.init()
            else:
                NotADirectoryError(root)
        return instance


def human_time_to_int(time: str) -> Optional[int]:
    if not time:
        return None

    suffix = time[-1]
    try:
        num = int(time if suffix.isdigit() else time[:-1])
    except ValueError:
        return None
    return num * {
        "h": 60 * 60,
        "d": 60 * 60 * 24,
        "w": 60 * 60 * 24 * 7,
        "m": 31 * 24 * 60 * 60,
        "y": 60 * 60 * 24 * 365,
    }.get(suffix.lower(), 1)


def time_to_str(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def sizeof_fmt(num, suffix=""):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            if not unit:
                return f"{num:4.0f}{suffix}"
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def force_create_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)
    elif not os.path.isdir(name):
        os.remove(name)
        os.mkdir(name)


def sql_str(s: str) -> str:
    s = s.replace("'", "''")
    return f"'{s}'"


def sql_file_filter(
    names=None,
    inames=None,
    type=None,  # pylint: disable=redefined-builtin
    op="GLOB",
):
    names_sql = (
        [f"name {op} {sql_str(name)}" for name in names] if names else []
    )
    inames_sql = (
        [f"lcase(name) {op} lcase({sql_str(iname)}')" for iname in inames]
        if inames
        else []
    )
    name_filter = " OR ".join(names_sql + inames_sql)

    type_filter = {
        "f": "dir_id IS NULL",
        "d": "dir_id IS NOT NULL",
        "": "",
        None: "",
    }.get(type, None)

    if type_filter is None:
        raise RuntimeError(f"Not supported 'type': {type}")

    if name_filter and type_filter:
        return f"({name_filter}) AND ({type_filter})"
    if name_filter:
        return f"({name_filter})"
    if type_filter:
        return f"({type_filter})"

    return ""


def dql_paths_join(
    source_path: str, file_paths: Iterable[str]
) -> Iterable[str]:
    source_parts = source_path.rstrip("/").split("/")
    if set(source_parts[-1]).intersection(GLOB_CHARS):
        # Remove last element if it is a glob match (such as *)
        source_parts.pop()
    source_stripped = "/".join(source_parts)
    return (f"{source_stripped}/{path.lstrip('/')}" for path in file_paths)


# From: https://docs.python.org/3/library/shutil.html#rmtree-example
def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)
