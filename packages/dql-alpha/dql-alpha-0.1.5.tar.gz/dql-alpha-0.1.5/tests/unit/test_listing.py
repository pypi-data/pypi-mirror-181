from datetime import datetime

import pytest

from dql.catalog import Catalog
from dql.listing import Listing

# pylint: disable=redefined-outer-name

TS = datetime(2022, 8, 1)
DB_FILE = ".test.db"

TREE = {
    "dir1": {
        "d2": {None: ["file1.csv", "file2.csv"]},
        None: ["dataset.csv"],
    },
    "dir2": {None: ["diagram.png"]},
    None: ["users.csv"],
}


def _tree_to_db(lst: Listing, tree: dict, dir_id: int = 0, path=""):
    for k, v in tree.items():
        if k:
            new_dir_id = lst.insert_dir(dir_id, k, TS, path)
            _tree_to_db(lst, v, new_dir_id, path + "/" + k)
        else:
            for fname in v:
                lst.insert_file(dir_id, fname, TS)


@pytest.fixture
def listing(data_storage):
    bkt = "s3://whatever"
    lst, _ = Catalog.enlist_source(data_storage, bkt, 1234, to_fetch=False)
    lst.insert_root()
    _tree_to_db(lst, TREE, 0)
    return lst


def test_resolve_path_in_root(listing):
    node = listing.resolve_path("dir1")
    assert node.dir_id
    assert node.name == "dir1"


def test_path_resolving_nested(listing):
    node = listing.resolve_path("dir1/d2/file2.csv")
    assert node.dir_id is None
    assert node.name == "file2.csv"
    assert not node.is_dir

    node = listing.resolve_path("dir1/d2")
    assert node.dir_id
    assert node.is_dir
    assert node.name == "d2"


def test_resolve_not_existing_path(listing):
    with pytest.raises(FileNotFoundError):
        listing.resolve_path("dir1/fake-file-name")


def test_resolve_root(listing):
    node = listing.resolve_path("")
    assert node.dir_id == 0
    assert node.name == ""


def test_path_starts_with_slash(listing):
    node = listing.resolve_path("/dir1")
    assert node.dir_id
    assert node.name == "dir1"


def test_dir_ends_with_slash(listing):
    node = listing.resolve_path("dir1/")
    assert node.dir_id
    assert node.name == "dir1"


def test_file_ends_with_slash(listing):
    with pytest.raises(FileNotFoundError):
        listing.resolve_path("dir1/dataset.csv/")


def _match_filenames(nodes, expected_names):
    assert len(nodes) == len(expected_names)
    names = (node.name for node in nodes)
    assert set(names).intersection(set(expected_names))


def test_basic_expansion(listing):
    nodes = listing.expand_path("*")
    _match_filenames(nodes, ["dir1", "dir2", "users.csv"])


def test_subname_expansion(listing):
    nodes = listing.expand_path("di*/")
    _match_filenames(nodes, ["dir1", "dir2"])


def test_multilevel_expansion(listing):
    nodes = listing.expand_path("dir[1,2]/d*")
    _match_filenames(nodes, ["dataset.csv", "diagram.png", "d2"])


def test_expand_root(listing):
    nodes = listing.expand_path("")
    assert len(nodes) == 1
    assert nodes[0].dir_id == 0


def test_list_dir(listing):
    dir1 = listing.resolve_path("dir1/")
    nodes = list(listing.ls_path(dir1))
    _match_filenames(nodes, ["dir2", "dataset.csv"])


def test_list_file(listing):
    file = listing.resolve_path("dir1/dataset.csv")
    nodes = list(listing.ls_path(file))
    _match_filenames(nodes, ["dataset.csv"])
    assert nodes[0].dir_id == file.dir_id
    assert nodes[0].name == file.name


def test_subtree(listing):
    dir1 = listing.resolve_path("dir1/")
    nodes = listing.data_storage.walk_subtree(dir1)
    subtree_files = ["dir2", "dataset.csv", "file1.csv", "file2.csv"]
    _match_filenames(list(nodes), subtree_files)
