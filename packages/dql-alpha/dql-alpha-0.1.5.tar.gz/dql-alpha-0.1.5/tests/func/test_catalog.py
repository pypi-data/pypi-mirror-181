import os
import shutil
import stat
from pathlib import PosixPath
from typing import Dict, NamedTuple

import pytest
import yaml
from upath.implementations.cloud import CloudPath

from dql.catalog import Catalog, parse_dql_file


class CloudTestCatalog(NamedTuple):
    src: CloudPath
    working_dir: PosixPath
    catalog: Catalog
    client_config: Dict[str, str]


class CloudTestServer(NamedTuple):
    src: CloudPath
    client_config: Dict[str, str]


# Test servers can be cached as they are not modified in these tests
cloud_server_cache: Dict[str, CloudTestServer] = {}


# From: https://docs.python.org/3/library/shutil.html#rmtree-example
def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)


@pytest.fixture
def cloud_test_catalog(request, tmp_path, tmp_upath_factory, data_storage):
    cloud_type = request.param
    if cloud_type in cloud_server_cache:
        src_path = cloud_server_cache[cloud_type].src
        client_config = cloud_server_cache[cloud_type].client_config
    else:
        src_path = tmp_upath_factory.mktemp(cloud_type)
        fs = src_path._accessor._fs  # pylint:disable=protected-access
        if cloud_type == "s3":
            endpoint_url = fs.client_kwargs["endpoint_url"]
            client_config = {"aws_endpoint_url": endpoint_url}
        elif cloud_type == "gcs":
            endpoint_url = fs._endpoint  # pylint:disable=protected-access
            client_config = {"endpoint_url": endpoint_url}
        (src_path / "description").write_text("Cats and Dogs")
        (src_path / "cats" / "cat1").write_text("meow")
        (src_path / "cats" / "cat2").write_text("mrow")
        (src_path / "dogs" / "dog1").write_text("woof")
        (src_path / "dogs" / "dog2").write_text("arf")
        (src_path / "dogs" / "dog3").write_text("bark")
        (src_path / "dogs" / "others" / "dog4").write_text("ruff")
        cloud_server_cache[cloud_type] = CloudTestServer(
            src=src_path,
            client_config=client_config,
        )

    cache_dir = tmp_path / ".dql" / "cache"
    cache_dir.mkdir(parents=True)
    tmpfile_dir = tmp_path / ".dql" / "tmp"
    tmpfile_dir.mkdir()

    catalog = Catalog(
        data_storage, cache_dir=str(cache_dir), tmp_dir=str(tmpfile_dir)
    )

    return CloudTestCatalog(
        src=src_path,
        working_dir=tmp_path,
        catalog=catalog,
        client_config=client_config,
    )


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
def test_find(cloud_test_catalog):
    src = cloud_test_catalog.src
    catalog = cloud_test_catalog.catalog
    config = cloud_test_catalog.client_config

    assert set(catalog.find([str(src)], client_config=config)) == {
        str(src / "description"),
        str(src / "cats") + "/",
        str(src / "cats" / "cat1"),
        str(src / "cats" / "cat2"),
        str(src / "dogs") + "/",
        str(src / "dogs" / "dog1"),
        str(src / "dogs" / "dog2"),
        str(src / "dogs" / "dog3"),
        str(src / "dogs" / "others") + "/",
        str(src / "dogs" / "others" / "dog4"),
    }

    with pytest.raises(FileNotFoundError):
        set(
            catalog.find(
                [str(src / "does_not_exist")],
                client_config=config,
            )
        )


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
@pytest.mark.parametrize(
    "recursive,star",
    ((True, True), (True, False), (False, True), (False, False)),
)
def test_cp_root(cloud_test_catalog, recursive, star):
    src = cloud_test_catalog.src
    working_dir = cloud_test_catalog.working_dir
    catalog = cloud_test_catalog.catalog

    dest = working_dir / "data"

    if star:
        src_path = f"{str(src).rstrip('/')}/*"
    else:
        src_path = str(src)

    catalog.cp(
        [src_path],
        str(dest),
        client_config=cloud_test_catalog.client_config,
        recursive=recursive,
    )

    if not star and not recursive:
        # The root directory is skipped, so nothing is copied
        assert (dest / "description").exists() is False
        assert (dest / "cats").exists() is False
        assert (dest / "dogs").exists() is False
        assert (dest / "others").exists() is False
        assert dest.with_suffix(".dql").exists() is False
        return

    assert (dest / "description").read_text() == "Cats and Dogs"

    # Testing DQL File Contents
    assert dest.with_suffix(".dql").is_file()
    dql_contents = yaml.safe_load(dest.with_suffix(".dql").read_text())
    assert len(dql_contents) == 1
    data = dql_contents[0]
    assert data["data-source"]["uri"] == src_path.rstrip("/")
    expected_file_count = 7 if recursive else 1
    assert len(data["files"]) == expected_file_count
    files_by_name = {f["name"]: f for f in data["files"]}

    # Directories should never be saved
    assert "cats" not in files_by_name
    assert "dogs" not in files_by_name
    assert "others" not in files_by_name
    assert "dogs/others" not in files_by_name

    # Ensure all files have checksum saved
    for f in data["files"]:
        assert len(f["checksum"]) > 1

    # Description is always copied (if anything is copied)
    prefix = "" if star else "/"
    assert files_by_name[f"{prefix}description"]["size"] == 13

    if recursive:
        assert (dest / "cats" / "cat1").read_text() == "meow"
        assert (dest / "cats" / "cat2").read_text() == "mrow"
        assert (dest / "dogs" / "dog1").read_text() == "woof"
        assert (dest / "dogs" / "dog2").read_text() == "arf"
        assert (dest / "dogs" / "dog3").read_text() == "bark"
        assert (dest / "dogs" / "others" / "dog4").read_text() == "ruff"
        assert files_by_name[f"{prefix}cats/cat1"]["size"] == 4
        assert files_by_name[f"{prefix}cats/cat2"]["size"] == 4
        assert files_by_name[f"{prefix}dogs/dog1"]["size"] == 4
        assert files_by_name[f"{prefix}dogs/dog2"]["size"] == 3
        assert files_by_name[f"{prefix}dogs/dog3"]["size"] == 4
        assert files_by_name[f"{prefix}dogs/others/dog4"]["size"] == 4
        return

    assert (dest / "cats").exists() is False
    assert (dest / "dogs").exists() is False
    for prefix in ["/", ""]:
        assert f"{prefix}cats/cat1" not in files_by_name
        assert f"{prefix}cats/cat2" not in files_by_name
        assert f"{prefix}dogs/dog1" not in files_by_name
        assert f"{prefix}dogs/dog2" not in files_by_name
        assert f"{prefix}dogs/dog3" not in files_by_name
        assert f"{prefix}dogs/others/dog4" not in files_by_name


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
@pytest.mark.parametrize(
    "recursive,star,slash",
    (
        (True, True, False),
        (True, False, False),
        (True, False, True),
        (False, True, False),
        (False, False, False),
        (False, False, True),
    ),
)
def test_cp_subdir(cloud_test_catalog, recursive, star, slash):
    src = cloud_test_catalog.src / "dogs"
    working_dir = cloud_test_catalog.working_dir
    catalog = cloud_test_catalog.catalog

    dest = working_dir / "data"

    if star:
        src_path = f"{str(src)}/*"
    else:
        src_path = str(src)
        if slash:
            src_path = f"{src_path}/"

    catalog.cp(
        [src_path],
        str(dest),
        client_config=cloud_test_catalog.client_config,
        recursive=recursive,
    )

    if not star and not recursive:
        # Directories are skipped, so nothing is copied
        assert (dest / "dog1").exists() is False
        assert (dest / "dog2").exists() is False
        assert (dest / "dog3").exists() is False
        assert (dest / "dogs").exists() is False
        assert (dest / "others").exists() is False
        assert dest.with_suffix(".dql").exists() is False
        return

    # Testing DQL File Contents
    assert dest.with_suffix(".dql").is_file()
    dql_contents = yaml.safe_load(dest.with_suffix(".dql").read_text())
    assert len(dql_contents) == 1
    data = dql_contents[0]
    assert data["data-source"]["uri"] == src_path.rstrip("/")
    expected_file_count = 4 if recursive else 3
    assert len(data["files"]) == expected_file_count
    files_by_name = {f["name"]: f for f in data["files"]}

    # Directories should never be saved
    assert "others" not in files_by_name
    assert "dogs/others" not in files_by_name

    # Ensure all files have checksum saved
    for f in data["files"]:
        assert len(f["checksum"]) > 1

    if star or slash:
        assert (dest / "dog1").read_text() == "woof"
        assert (dest / "dog2").read_text() == "arf"
        assert (dest / "dog3").read_text() == "bark"
        assert (dest / "dogs").exists() is False
        assert files_by_name["dog1"]["size"] == 4
        assert files_by_name["dog2"]["size"] == 3
        assert files_by_name["dog3"]["size"] == 4
        if recursive:
            assert (dest / "others" / "dog4").read_text() == "ruff"
            assert files_by_name["others/dog4"]["size"] == 4
        else:
            assert (dest / "others").exists() is False
            assert "others/dog4" not in files_by_name
        return

    assert (dest / "dogs" / "dog1").read_text() == "woof"
    assert (dest / "dogs" / "dog2").read_text() == "arf"
    assert (dest / "dogs" / "dog3").read_text() == "bark"
    assert (dest / "dogs" / "others" / "dog4").read_text() == "ruff"
    assert (dest / "dog1").exists() is False
    assert (dest / "dog2").exists() is False
    assert (dest / "dog3").exists() is False
    assert (dest / "others").exists() is False
    assert files_by_name["dogs/dog1"]["size"] == 4
    assert files_by_name["dogs/dog2"]["size"] == 3
    assert files_by_name["dogs/dog3"]["size"] == 4
    assert files_by_name["dogs/others/dog4"]["size"] == 4


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
@pytest.mark.parametrize(
    "recursive,star,slash",
    (
        (True, True, False),
        (True, False, False),
        (True, False, True),
        (False, True, False),
        (False, False, False),
        (False, False, True),
    ),
)
def test_cp_multi_subdir(cloud_test_catalog, recursive, star, slash):
    sources = [
        cloud_test_catalog.src / "cats",
        cloud_test_catalog.src / "dogs",
    ]
    working_dir = cloud_test_catalog.working_dir
    catalog = cloud_test_catalog.catalog

    dest = working_dir / "data"

    if star:
        src_paths = [f"{str(src)}/*" for src in sources]
    else:
        src_paths = [str(src) for src in sources]
        if slash:
            src_paths = [f"{src}/" for src in src_paths]

    catalog.cp(
        src_paths,
        str(dest),
        client_config=cloud_test_catalog.client_config,
        recursive=recursive,
    )

    if not star and not recursive:
        # Directories are skipped, so nothing is copied
        assert (dest / "cat1").exists() is False
        assert (dest / "cat2").exists() is False
        assert (dest / "cats").exists() is False
        assert (dest / "dog1").exists() is False
        assert (dest / "dog2").exists() is False
        assert (dest / "dog3").exists() is False
        assert (dest / "dogs").exists() is False
        assert (dest / "others").exists() is False
        assert dest.with_suffix(".dql").exists() is False
        return

    # Testing DQL File Contents
    assert dest.with_suffix(".dql").is_file()
    dql_contents = yaml.safe_load(dest.with_suffix(".dql").read_text())
    assert len(dql_contents) == 2
    data_cats = dql_contents[0]
    data_dogs = dql_contents[1]
    assert data_cats["data-source"]["uri"] == src_paths[0].rstrip("/")
    assert data_dogs["data-source"]["uri"] == src_paths[1].rstrip("/")
    assert len(data_cats["files"]) == 2
    assert len(data_dogs["files"]) == 4 if recursive else 3
    cat_files_by_name = {f["name"]: f for f in data_cats["files"]}
    dog_files_by_name = {f["name"]: f for f in data_dogs["files"]}

    # Directories should never be saved
    assert "others" not in dog_files_by_name
    assert "dogs/others" not in dog_files_by_name

    # Ensure all files have checksum saved
    for f in data_cats["files"]:
        assert len(f["checksum"]) > 1
    for f in data_dogs["files"]:
        assert len(f["checksum"]) > 1

    if star or slash:
        assert (dest / "cat1").read_text() == "meow"
        assert (dest / "cat2").read_text() == "mrow"
        assert (dest / "dog1").read_text() == "woof"
        assert (dest / "dog2").read_text() == "arf"
        assert (dest / "dog3").read_text() == "bark"
        assert (dest / "cats").exists() is False
        assert (dest / "dogs").exists() is False
        assert cat_files_by_name["cat1"]["size"] == 4
        assert cat_files_by_name["cat2"]["size"] == 4
        assert dog_files_by_name["dog1"]["size"] == 4
        assert dog_files_by_name["dog2"]["size"] == 3
        assert dog_files_by_name["dog3"]["size"] == 4
        if recursive:
            assert (dest / "others" / "dog4").read_text() == "ruff"
            assert dog_files_by_name["others/dog4"]["size"] == 4
        else:
            assert (dest / "others").exists() is False
            assert "others/dog4" not in dog_files_by_name
        return

    assert (dest / "cats" / "cat1").read_text() == "meow"
    assert (dest / "cats" / "cat2").read_text() == "mrow"
    assert (dest / "dogs" / "dog1").read_text() == "woof"
    assert (dest / "dogs" / "dog2").read_text() == "arf"
    assert (dest / "dogs" / "dog3").read_text() == "bark"
    assert (dest / "dogs" / "others" / "dog4").read_text() == "ruff"
    assert (dest / "cat1").exists() is False
    assert (dest / "cat2").exists() is False
    assert (dest / "dog1").exists() is False
    assert (dest / "dog2").exists() is False
    assert (dest / "dog3").exists() is False
    assert (dest / "others").exists() is False
    assert cat_files_by_name["cats/cat1"]["size"] == 4
    assert cat_files_by_name["cats/cat2"]["size"] == 4
    assert dog_files_by_name["dogs/dog1"]["size"] == 4
    assert dog_files_by_name["dogs/dog2"]["size"] == 3
    assert dog_files_by_name["dogs/dog3"]["size"] == 4
    assert dog_files_by_name["dogs/others/dog4"]["size"] == 4


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
def test_cp_double_subdir(cloud_test_catalog):
    src = cloud_test_catalog.src / "dogs" / "others"
    working_dir = cloud_test_catalog.working_dir
    catalog = cloud_test_catalog.catalog

    dest = working_dir / "data"

    src_path = f"{str(src)}/"

    catalog.cp(
        [src_path],
        str(dest),
        client_config=cloud_test_catalog.client_config,
        recursive=True,
    )

    # Testing DQL File Contents
    assert dest.with_suffix(".dql").is_file()
    dql_contents = yaml.safe_load(dest.with_suffix(".dql").read_text())
    assert len(dql_contents) == 1
    data = dql_contents[0]
    assert data["data-source"]["uri"] == src_path.rstrip("/")
    assert len(data["files"]) == 1
    files_by_name = {f["name"]: f for f in data["files"]}

    # Directories should never be saved
    assert "others" not in files_by_name
    assert "dogs/others" not in files_by_name

    # Ensure all files have checksum saved
    for f in data["files"]:
        assert len(f["checksum"]) > 1

    assert (dest / "dogs").exists() is False
    assert (dest / "others").exists() is False
    assert (dest / "dog4").read_text() == "ruff"
    assert files_by_name["dog4"]["size"] == 4


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
def test_cp_dql_file_options(cloud_test_catalog):
    src = cloud_test_catalog.src / "dogs"
    working_dir = cloud_test_catalog.working_dir
    catalog = cloud_test_catalog.catalog

    dest = working_dir / "data"

    src_path = str(src / "*")

    dql_file = working_dir / "custom_name.dql"

    catalog.cp(
        [src_path],
        str(dest),
        client_config=cloud_test_catalog.client_config,
        recursive=False,
        dql_only=True,
        dql_file=str(dql_file),
    )

    assert (dest / "dog1").exists() is False
    assert (dest / "dog2").exists() is False
    assert (dest / "dog3").exists() is False
    assert (dest / "dogs").exists() is False
    assert (dest / "others").exists() is False
    assert dest.with_suffix(".dql").exists() is False

    # Testing DQL File Contents
    assert dql_file.is_file()
    dql_contents = yaml.safe_load(dql_file.read_text())
    assert len(dql_contents) == 1
    data = dql_contents[0]
    assert data["data-source"]["uri"] == src_path.rstrip("/")
    expected_file_count = 3
    assert len(data["files"]) == expected_file_count
    files_by_name = {f["name"]: f for f in data["files"]}

    assert parse_dql_file(str(dql_file)) == dql_contents

    # Directories should never be saved
    assert "others" not in files_by_name
    assert "dogs/others" not in files_by_name

    assert files_by_name["dog1"]["size"] == 4
    assert files_by_name["dog2"]["size"] == 3
    assert files_by_name["dog3"]["size"] == 4
    assert "others/dog4" not in files_by_name

    with pytest.raises(FileNotFoundError):
        # Should fail, as * will not be expanded
        catalog.cp(
            [src_path],
            str(dest),
            client_config=cloud_test_catalog.client_config,
            recursive=False,
            dql_only=True,
            dql_file=str(dql_file),
            no_glob=True,
        )


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
def test_cp_dql_file_sources(cloud_test_catalog):
    sources = [
        f"{str(cloud_test_catalog.src / 'cats')}/",
        str(cloud_test_catalog.src / "dogs" / "*"),
    ]
    working_dir = cloud_test_catalog.working_dir
    catalog = cloud_test_catalog.catalog

    dest = working_dir / "data"

    dql_files = [
        working_dir / "custom_cats.dql",
        working_dir / "custom_dogs.dql",
    ]

    catalog.cp(
        sources[:1],
        str(dest),
        client_config=cloud_test_catalog.client_config,
        recursive=True,
        dql_only=True,
        dql_file=str(dql_files[0]),
    )

    catalog.cp(
        sources[1:],
        str(dest),
        client_config=cloud_test_catalog.client_config,
        recursive=True,
        dql_only=True,
        dql_file=str(dql_files[1]),
    )

    # Files should not be copied yet
    assert (dest / "cat1").exists() is False
    assert (dest / "cat2").exists() is False
    assert (dest / "cats").exists() is False
    assert (dest / "dog1").exists() is False
    assert (dest / "dog2").exists() is False
    assert (dest / "dog3").exists() is False
    assert (dest / "dogs").exists() is False
    assert (dest / "others").exists() is False

    # Testing DQL File Contents
    dql_data = []
    for dqf in dql_files:
        assert dqf.is_file()
        dql_contents = yaml.safe_load(dqf.read_text())
        assert len(dql_contents) == 1
        dql_data.extend(dql_contents)

    assert len(dql_data) == 2
    data_cats1 = dql_data[0]
    data_dogs1 = dql_data[1]
    assert data_cats1["data-source"]["uri"] == sources[0].rstrip("/")
    assert data_dogs1["data-source"]["uri"] == sources[1].rstrip("/")
    assert len(data_cats1["files"]) == 2
    assert len(data_dogs1["files"]) == 4
    cat_files_by_name1 = {f["name"]: f for f in data_cats1["files"]}
    dog_files_by_name1 = {f["name"]: f for f in data_dogs1["files"]}

    # Directories should never be saved
    assert "others" not in dog_files_by_name1
    assert "dogs/others" not in dog_files_by_name1

    assert cat_files_by_name1["cat1"]["size"] == 4
    assert cat_files_by_name1["cat2"]["size"] == 4
    assert dog_files_by_name1["dog1"]["size"] == 4
    assert dog_files_by_name1["dog2"]["size"] == 3
    assert dog_files_by_name1["dog3"]["size"] == 4
    assert dog_files_by_name1["others/dog4"]["size"] == 4

    # Copy using these DQL files as sources
    catalog.cp(
        [str(dqf) for dqf in dql_files],
        str(dest),
        client_config=cloud_test_catalog.client_config,
        recursive=True,
    )

    # Files should now be copied
    assert (dest / "cat1").read_text() == "meow"
    assert (dest / "cat2").read_text() == "mrow"
    assert (dest / "dog1").read_text() == "woof"
    assert (dest / "dog2").read_text() == "arf"
    assert (dest / "dog3").read_text() == "bark"
    assert (dest / "others" / "dog4").read_text() == "ruff"

    # Testing DQL File Contents
    assert dest.with_suffix(".dql").is_file()
    dql_contents = yaml.safe_load(dest.with_suffix(".dql").read_text())
    assert len(dql_contents) == 2
    data_cats2 = dql_contents[0]
    data_dogs2 = dql_contents[1]
    assert data_cats2["data-source"]["uri"] == sources[0].rstrip("/")
    assert data_dogs2["data-source"]["uri"] == sources[1].rstrip("/")
    assert len(data_cats2["files"]) == 2
    assert len(data_dogs2["files"]) == 4
    cat_files_by_name2 = {f["name"]: f for f in data_cats2["files"]}
    dog_files_by_name2 = {f["name"]: f for f in data_dogs2["files"]}

    # Ensure all files have checksum saved
    for f in data_cats2["files"]:
        assert len(f["checksum"]) > 1
    for f in data_dogs2["files"]:
        assert len(f["checksum"]) > 1

    # Directories should never be saved
    assert "others" not in dog_files_by_name2
    assert "dogs/others" not in dog_files_by_name2

    assert cat_files_by_name2["cat1"]["size"] == 4
    assert cat_files_by_name2["cat2"]["size"] == 4
    assert dog_files_by_name2["dog1"]["size"] == 4
    assert dog_files_by_name2["dog2"]["size"] == 3
    assert dog_files_by_name2["dog3"]["size"] == 4
    assert dog_files_by_name2["others/dog4"]["size"] == 4


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
def test_get(cloud_test_catalog):
    src = cloud_test_catalog.src
    catalog = cloud_test_catalog.catalog
    config = cloud_test_catalog.client_config
    dest = cloud_test_catalog.working_dir / "data"

    catalog.get(str(src), str(dest), client_config=config)

    assert (dest / "cats" / "cat1").read_text() == "meow"
    assert (dest / "cats" / "cat2").read_text() == "mrow"
    assert (dest / "dogs" / "dog1").read_text() == "woof"
    assert (dest / "dogs" / "dog2").read_text() == "arf"
    assert (dest / "dogs" / "dog3").read_text() == "bark"
    assert (dest / "dogs" / "others" / "dog4").read_text() == "ruff"
    assert dest.with_suffix(".dql").is_file()


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
def test_get_subdir(cloud_test_catalog):
    src = f"{str(cloud_test_catalog.src)}/dogs"
    working_dir = cloud_test_catalog.working_dir
    catalog = cloud_test_catalog.catalog

    dest = working_dir / "data"

    catalog.get(src, str(dest), client_config=cloud_test_catalog.client_config)

    assert dest.with_suffix(".dql").is_file()
    assert (dest / "dog1").read_text() == "woof"
    assert (dest / "dog2").read_text() == "arf"
    assert (dest / "dog3").read_text() == "bark"
    assert (dest / "dogs").exists() is False
    assert (dest / "others" / "dog4").read_text() == "ruff"

    assert parse_dql_file(str(dest.with_suffix(".dql"))) == [
        yaml.safe_load(dest.with_suffix(".dql").read_text())
    ]

    with pytest.raises(RuntimeError):
        # An error should be raised if the output directory already exists
        catalog.get(
            src, str(dest), client_config=cloud_test_catalog.client_config
        )

    shutil.rmtree(dest, onerror=remove_readonly)
    assert dest.with_suffix(".dql").is_file()

    with pytest.raises(RuntimeError):
        # An error should also be raised if the dataset file already exists
        catalog.get(
            src, str(dest), client_config=cloud_test_catalog.client_config
        )


@pytest.mark.parametrize("cloud_test_catalog", ["s3", "gcs"], indirect=True)
def test_ls_glob(cloud_test_catalog):
    src = cloud_test_catalog.src
    catalog = cloud_test_catalog.catalog

    assert [
        (source.node.name, [n.name for n in nodes])
        for source, nodes in catalog.ls(
            [str(src / "dogs" / "dog*")],
            client_config=cloud_test_catalog.client_config,
        )
    ] == [("dog1", ["dog1"]), ("dog2", ["dog2"]), ("dog3", ["dog3"])]
