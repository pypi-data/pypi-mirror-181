import pytest

from dql.utils import dql_paths_join

DQL_TEST_PATHS = ["/file1", "file2", "/dir/file3", "dir/file4"]
DQL_EX_ROOT = ["/file1", "/file2", "/dir/file3", "/dir/file4"]
DQL_EX_SUBDIR = [
    "subdir/file1",
    "subdir/file2",
    "subdir/dir/file3",
    "subdir/dir/file4",
]
DQL_EX_DOUBLE_SUBDIR = [
    "subdir/double/file1",
    "subdir/double/file2",
    "subdir/double/dir/file3",
    "subdir/double/dir/file4",
]


@pytest.mark.parametrize(
    "src,paths,expected",
    (
        ("", DQL_TEST_PATHS, DQL_EX_ROOT),
        ("/", DQL_TEST_PATHS, DQL_EX_ROOT),
        ("/*", DQL_TEST_PATHS, DQL_EX_ROOT),
        ("/file*", DQL_TEST_PATHS, DQL_EX_ROOT),
        ("subdir", DQL_TEST_PATHS, DQL_EX_SUBDIR),
        ("subdir/", DQL_TEST_PATHS, DQL_EX_SUBDIR),
        ("subdir/*", DQL_TEST_PATHS, DQL_EX_SUBDIR),
        ("subdir/file*", DQL_TEST_PATHS, DQL_EX_SUBDIR),
        ("subdir/double", DQL_TEST_PATHS, DQL_EX_DOUBLE_SUBDIR),
        ("subdir/double/", DQL_TEST_PATHS, DQL_EX_DOUBLE_SUBDIR),
        ("subdir/double/*", DQL_TEST_PATHS, DQL_EX_DOUBLE_SUBDIR),
        ("subdir/double/file*", DQL_TEST_PATHS, DQL_EX_DOUBLE_SUBDIR),
    ),
)
def test_dql_paths_join(src, paths, expected):
    assert list(dql_paths_join(src, paths)) == expected
