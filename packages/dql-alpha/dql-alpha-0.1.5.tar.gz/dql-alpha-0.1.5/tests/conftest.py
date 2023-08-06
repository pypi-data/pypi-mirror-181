import os

import pytest

from dql.data_storage import DefaultDataStorage

DEFAULT_DQL_BIN = "dql"
DEFAULT_DQL_GIT_REPO = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


@pytest.fixture
def data_storage():
    _data_storage = DefaultDataStorage(db_file=":memory:")
    return _data_storage


@pytest.fixture
def tmp_dir(tmp_path_factory, monkeypatch):
    dpath = tmp_path_factory.mktemp("dql-test")
    monkeypatch.chdir(dpath)
    return dpath


def pytest_addoption(parser):
    parser.addoption(
        "--dql-bin",
        type=str,
        default=DEFAULT_DQL_BIN,
        help="Path to dql binary",
    )

    parser.addoption(
        "--dql-revs",
        type=str,
        help=(
            "Comma-separated list of DQL revisions to test "
            "(overrides `--dql-bin`)"
        ),
    )

    parser.addoption(
        "--dql-git-repo",
        type=str,
        default=DEFAULT_DQL_GIT_REPO,
        help="Path or url to dql git repo",
    )


class DQLTestConfig:
    def __init__(self):
        self.dql_bin = DEFAULT_DQL_BIN
        self.dql_revs = None
        self.dql_git_repo = DEFAULT_DQL_GIT_REPO


@pytest.fixture(scope="session")
def test_config(request):
    return request.config.dql_config


def pytest_configure(config):
    config.dql_config = DQLTestConfig()

    config.dql_config.dql_bin = config.getoption("--dql-bin")
    config.dql_config.dql_revs = config.getoption("--dql-revs")
    config.dql_config.dql_git_repo = config.getoption("--dql-git-repo")
