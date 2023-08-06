from datetime import datetime, timedelta

import pytest

from dql import utils
from dql.client import Client
from dql.listing import Listing
from dql.storage import Storage

TS = datetime(2022, 8, 1)
EXPIRES = datetime(2022, 8, 2)


def test_human_time():
    assert utils.human_time_to_int("1236") == 1236
    assert utils.human_time_to_int("3h") == 3 * 60 * 60
    assert utils.human_time_to_int("2w") == 2 * 7 * 24 * 60 * 60
    assert utils.human_time_to_int("4M") == 4 * 31 * 24 * 60 * 60

    assert utils.human_time_to_int("bla") is None


def test_storage():
    s = Storage("ID", "s3", "foo", TS, EXPIRES)
    assert s.root_node.dir_id == 0

    d = s.to_dict()
    assert d.get("uri") == s.uri


def test_expiration_time():
    assert Storage.get_expiration_time(TS, 12344) == TS + timedelta(
        seconds=12344
    )


def test_adding_storage(data_storage):
    client, _ = Client.parse_url("s3://whatever")
    storage = client.as_record()
    cached_storage = data_storage.get_storage(
        storage.id, storage.timestamp_str
    )
    assert cached_storage is None

    _ = Listing(storage, data_storage, client)
    data_storage.register_storage_for_indexing(storage)

    cnt = data_storage.db.execute("SELECT COUNT() FROM buckets").fetchall()
    assert cnt[0][0] == 1

    query = "SELECT * FROM buckets WHERE id = ?"
    bkt = data_storage.db.execute(query, [storage.id]).fetchall()
    assert len(bkt) == 1

    s = Storage(*bkt[0])
    assert s == storage


@pytest.mark.parametrize(
    "ttl",
    (-1, 999999999999, 99999999999999, 9999999999999999),
)
def test_max_ttl(data_storage, ttl):  # pylint: disable=unused-argument
    client, _ = Client.parse_url("s3://whatever")
    expires = Storage.get_expiration_time(TS, ttl)
    storage = Storage(
        client.storage_id, client.protocol, client.name, TS, expires
    )
    assert storage.timestamp == TS
    assert storage.expires == datetime.max
    assert storage.timestamp_str  # no error
    assert storage.timestamp_to_local  # no error
    assert storage.expires_to_local  # no error


def test_storage_without_dates(
    data_storage,
):  # pylint: disable=unused-argument
    client, _ = Client.parse_url("s3://whatever")
    storage = Storage(
        client.storage_id, client.protocol, client.name, None, None
    )
    assert storage.timestamp is None
    assert storage.expires is None
    assert storage.timestamp_str is None  # no error
    assert storage.timestamp_to_local is None  # no error
    assert storage.expires_to_local is None  # no error
    assert storage.to_dict() == {
        "uri": storage.uri,
        "timestamp": None,
        "expires": None,
    }
